import datetime
import hashlib
from typing import List, Optional, Union

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from fastapi import status
import jwt

from voter import tables
from voter.settings import setting

from voter.database import get_session, Session
from voter.models.users import UserOut, Token, UserCreate


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    return User.verify_token(token)


class User:
    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return bcrypt.verify(password, hashed_password)

    @classmethod
    def verify_token(cls, token: str) -> UserOut:
        exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Could not validate credentials',
                                  headers={'WWW-Authenticate': 'Bearer'}, )
        try:
            payload = jwt.decode(token, setting.jwt_secret, algorithms=setting.jwt_algorithms)
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            raise exception
        user_data = payload.get("user")
        try:
            user = UserOut.parse_obj(user_data)
        except ValidationError:
            raise exception
        return user

    @classmethod
    def create_token(cls, user: tables.Users) -> Token:
        user_data = UserOut.from_orm(user)
        now = datetime.datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + datetime.timedelta(seconds=setting.jwt_expires_s),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(payload, setting.jwt_secret, algorithm=setting.jwt_algorithms)

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.id = None
        self.session = session

    async def register_new_user(self, user_data: UserCreate) -> Token:
        user = tables.Users(email=user_data.email,
                            username=user_data.username,
                            hashed_password=self.hash_password(user_data.password))
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    async def auth_user(self, user_name: str, password: str) -> Token:
        user = self.session.query(tables.Users).filter_by(username=user_name).first()
        exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Incorrect username or password',
                                  headers={'WWW-Authenticate': 'Bearer'},
                                  )
        if not user:
            raise exception

        if not self.verify_password(password, user.hashed_password):
            raise exception
        return self.create_token(user)


#TODO  Регистарция по почте.