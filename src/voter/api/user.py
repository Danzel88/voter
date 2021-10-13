from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from voter.models.users import UserIn, UserOut, UserAuth
from voter.services.user import User

router = APIRouter(prefix="/auth")


@router.post("/sign-up", response_model=UserOut)
async def create_user(user: UserIn, service: User = Depends()):
    return await service.create_user(user)


@router.post("/sign-in", response_model=UserOut)
async def get_user(user: UserAuth, service: User = Depends(), ):
    return await service.get_user(user)


@router.post("/")
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)

#TODO реализовать аутентификацию потокену