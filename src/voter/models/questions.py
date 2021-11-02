import datetime
from typing import Optional

from pydantic import BaseModel, Field


class QuestionIn(BaseModel):
    text: str
    created_date: datetime.date

    class Config:
        orm_mode = True


class QuestionOut(QuestionIn):
    id: int
    author: int
    pros: Optional[int] = 0
    cons: Optional[int] = 0
    is_active: bool


class QuestionsResults(BaseModel):
    text: str
    created_date: datetime.date
    id: int
    pros: int
    cons: int
    presence: str
