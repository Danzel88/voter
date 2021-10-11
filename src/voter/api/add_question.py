from typing import List

from fastapi import APIRouter, Depends

from voter.models.choice import Choice
from voter.models.questions import QuestionIn, QuestionOut
from voter.services.create_question import QuestionsService

router = APIRouter(prefix="")


@router.get("/", response_model=List)
async def show_questions(service: QuestionsService = Depends()):
    return service.get_questions()


@router.post("/add", response_model=QuestionOut)
async def create_question(question_data: QuestionIn,
                          service: QuestionsService = Depends()):
    return service.create_question(question_data)


@router.patch("/vote", response_model=QuestionOut)
async def update_question(question_id: int, choice: Choice,
                          service: QuestionsService = Depends()):
    return service.update_question(question_id, choice)
