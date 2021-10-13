from datetime import datetime
from typing import Optional

from pydantic import EmailStr, BaseModel, UUID4, Field


class UserIn(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    email: str
    password: str
