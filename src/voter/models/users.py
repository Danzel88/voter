from pydantic import EmailStr, BaseModel


class BaseUser(BaseModel):
    email: EmailStr
    username: str


class UserCreate(BaseUser):
    password: str


class UserOut(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
