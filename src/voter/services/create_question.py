from fastapi import Depends

from sqlalchemy.orm import Session

from voter import tables
from voter.database import get_session
from voter.models.questions import QuestionIn


class QuestionsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_questions(self) -> tables.Questions:
        all_questions = self.session.query(tables.Questions).all()
        return all_questions

    def create_question(self, question: QuestionIn) -> tables.Questions:
        question_data = tables.Questions(**question.dict())
        self.session.add(question_data)
        self.session.commit()
        return question_data
