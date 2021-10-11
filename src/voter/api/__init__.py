from fastapi import APIRouter

from .add_question import router as question_router

router = APIRouter()

router.include_router(question_router)


