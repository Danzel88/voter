from typing import Union

from fastapi import Depends, HTTPException, status

from sqlalchemy import func, insert
from sqlalchemy.orm import Session

from voter import tables
from voter.database import get_session
from voter.models.choice import Choice, BaseChoice
from voter.models.questions import QuestionIn, QuestionOut, QuestionsResults
from voter.services.exceptions import ALLREADY_VOTED_EXCEPTION


class QuestionsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _check_vote(self, question_id: int, user_id: int):
        """ Проверяем в талице 'Voted', если 'user_id' уже голосовал за 'question_id',
            возвращаем нужный статус """
        midterm_vote = self.session.query(tables.Voted) \
            .filter_by(question_id=question_id).filter_by(user_id=user_id).first()
        if midterm_vote is not None:
            if midterm_vote.user_id == user_id:
                raise ALLREADY_VOTED_EXCEPTION
        return True

    def _account_voting(self, question_id: int, user_id: int, choice: BaseChoice):
        """ Пишем в таблицу 'Voted'  'question_id' 'user_id' и 'name' из таблицы 'Choices'.
            'Voted' промежуточная таблица для подсчета результатов"""
        data_of_voted = (insert(tables.Voted).values(question_id=question_id,
                                                     user_id=user_id,
                                                     choices_names=choice))
        self.session.execute(data_of_voted)
        self.session.commit()

    def _get(self, question_id: int) -> tables.Questions:
        question = self.session.query(tables.Questions) \
            .filter_by(id=question_id).first()
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return question

    def get_questions_list(self, user_id: int) -> tables.Questions:
        all_questions = self.session.query(tables.Questions).filter_by(author=user_id).all()
        return all_questions

    def create_question(self, user_id: int, question: QuestionIn) -> tables.Questions:
        question_data = tables.Questions(**question.dict(), author=user_id)
        self.session.add(question_data)
        self.session.commit()
        return question_data

    def update_question(self, question_id: int, choice: BaseChoice):
        if choice == Choice.PROS.value:
            self.session.query(tables.Questions).filter_by(id=question_id) \
                .update({tables.Questions.pros: tables.Questions.pros + 1})
            self.session.commit()
        else:
            self.session.query(tables.Questions).filter_by(id=question_id) \
                .update({tables.Questions.cons: tables.Questions.cons + 1})
            self.session.commit()

    def write_vote_in_db(self, user_id: int, question_id: int, choice: BaseChoice) -> tables.Questions:
        """ Проверяем запись по 'question_id' в 'Questions', проверяем по 'user_id' в 'Voted',
        пишем в 'Voted' и обновляем 'за'/'против' в 'Questions' """
        if self._get(question_id) and self._check_vote(question_id, user_id):
            self._account_voting(question_id, user_id, choice)
            self.update_question(question_id, choice)
        return self._get(question_id)

    def get_voting_results(self) -> tables.Questions:
        query = self.session.execute('''select q.text, q.created_date, q.id, q.pros, 
        q.cons, count(distinct(v.user_id))*100/4 as presence from questions q join voted v 
        on q.id=v.question_id group by q.id''').all()
        return query
