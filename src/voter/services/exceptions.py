from fastapi import HTTPException
from fastapi import status


NOT_FOUND_QUESTION_EXCEPTION = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                             detail='The requested question was not found')
ALLREADY_VOTED_EXCEPTION = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                         detail='Your vote has already been counted')