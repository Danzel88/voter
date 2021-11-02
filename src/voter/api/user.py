from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from voter.models.users import UserCreate, UserOut
from voter.services.user import User, Token, get_current_user

router = APIRouter(prefix="/auth")


@router.post("/sign-up", response_model=Token)
async def create_user(user: UserCreate, service: User = Depends()):
    return await service.register_new_user(user)


@router.post("/sign-in", response_model=Token)
async def auth_user(user: OAuth2PasswordRequestForm = Depends(),
                    service: User = Depends()):
    return await service.auth_user(user.username, user.password)


@router.get("/user", response_model=UserOut)
async def get_user(user: User = Depends(get_current_user)):
    return user


#TODO ограничения прав доступа