from typing import List

from fastapi import APIRouter, Depends

from voter.models.questions import QuestionIn, QuestionOut
from voter.services.create_question import QuestionsService

router = APIRouter(prefix="/add")


@router.post("", response_model=QuestionOut)
async def create_questions(question_data: QuestionIn,
                           service: QuestionsService = Depends()):
    return service.create_question(question_data)


@router.get("", response_model=List)
async def show_questions(service: QuestionsService = Depends()):
    return service.get_questions()

