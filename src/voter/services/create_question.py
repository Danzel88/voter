from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from voter import tables
from voter.database import get_session
from voter.models.choice import Choice
from voter.models.questions import QuestionIn, QuestionOut


class QuestionsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, question_id: int) -> QuestionOut:
        question = self.session.query(tables.Questions).filter_by(id=question_id)\
            .first()
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return question

    def get_questions(self) -> tables.Questions:
        all_questions = self.session.query(tables.Questions).all()
        return all_questions

    def create_question(self, question: QuestionIn) -> tables.Questions:
        question_data = tables.Questions(**question.dict())
        self.session.add(question_data)
        self.session.commit()
        return question_data

    def update_question(self, question_id: int, choice: Choice) -> QuestionOut:
        if choice.value == Choice.PROS.value:
            self.session.query(tables.Questions).filter_by(id=question_id)\
                .update({tables.Questions.pros: tables.Questions.pros + 1})
            self.session.commit()
        else:
            self.session.query(tables.Questions).filter_by(id=question_id)\
                .update({tables.Questions.cons: tables.Questions.cons + 1})
            self.session.commit()
        return self._get(question_id)
