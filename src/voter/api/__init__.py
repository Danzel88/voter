from fastapi import APIRouter

from .question import router as question_router
from .user import router as user_router

router = APIRouter()

router.include_router(question_router)
router.include_router(user_router)


