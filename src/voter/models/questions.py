import datetime
from typing import Optional

from pydantic import BaseModel


class QuestionIn(BaseModel):
    text: str
    is_active: bool
    author: int
    created_date: datetime.date

    class Config:
        orm_mode = True


class QuestionOut(QuestionIn):
    id: int
    pros: Optional[int] = 0
    cons: Optional[int] = 0
    created_date: datetime.date
