from typing import List

from fastapi import APIRouter, Depends

from voter.models.choice import Choice
from voter.models.questions import QuestionIn, QuestionOut, QuestionsResults
from voter.services.question import QuestionsService
from voter.services.user import User, get_current_user

router = APIRouter(prefix="")


@router.get("/", response_model=List[QuestionOut])
async def show_questions(service: QuestionsService = Depends(),
                         user: User = Depends(get_current_user)):
    return service.get_questions_list(user_id=user.id)


@router.get("/results", response_model=List[QuestionsResults])
async def show_voting_results(service: QuestionsService = Depends(),
                              user: User = Depends(get_current_user)):
    return service.get_voting_results()


@router.post("/", response_model=QuestionOut)
async def create_question(question_data: QuestionIn,
                          service: QuestionsService = Depends(),
                          user: User = Depends(get_current_user)):
    return service.create_question(user_id=user.id, question=question_data)


@router.patch("/", response_model=QuestionOut)
async def update_question(question_id: int, choice: Choice,
                          service: QuestionsService = Depends(),
                          user: User = Depends(get_current_user)):
    return service.write_vote_in_db(user.id, question_id, choice.value)
