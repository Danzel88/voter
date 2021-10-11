from pydantic import BaseModel


class BaseChoice(BaseModel):
    id: int
    pros: str
    cons: str

    class Config:
        orm_mode = True
