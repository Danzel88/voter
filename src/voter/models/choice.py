from enum import Enum

from pydantic import BaseModel


class Choice(Enum):
    PROS = "За"
    CONS = "Против"


class BaseChoice(BaseModel):
    id: int
    name: Choice

    class Config:
        orm_mode = True
