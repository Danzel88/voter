import hashlib
from typing import List, Optional, Union

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import status

from voter import tables
from voter.settings import setting
from voter.database import get_session
from voter.models.users import UserIn, UserAuth


class User:
    def __init__(self, session=Depends(get_session)):
        self.session = session

    @classmethod
    def hash_password(cls, password: str, salt: str = setting.salt) -> str:
        return hashlib.sha256((password + salt).encode()).hexdigest().lower()

    def verify_password(self, email: str, password: str, orig_password: str, salt: str = setting.salt) -> bool:
        hash_password = self.hash_password(password, salt)
        # orig_password = self.session.query(tables.Users.hashed_password).filter_by(email=email).first()
        return hash_password == orig_password

    async def get_user_by_email(self, email: str) -> List[tables.Users]:
        query = self.session.query(tables.Users).filter_by(email=email).first()
        return await query

    async def create_user(self, user_data: UserIn) -> List[tables.Users]:
        user = tables.Users(
            email=user_data.email,
            name=user_data.name,
            hashed_password=self.hash_password(user_data.password))
        try:
            self.session.add(user)
            self.session.commit()
            return user
        except IntegrityError:
            return user

    async def get_user(self, user_data: UserAuth) -> List[tables.Users]:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password')
        user = self.session.query(tables.Users).filter_by(email=user_data.email).first()
        if not user or not self.verify_password(user_data.email, user_data.password, user.hashed_password):
            raise exception
        return user

#TODO реализовать генерацию и валидацию JWT токкена