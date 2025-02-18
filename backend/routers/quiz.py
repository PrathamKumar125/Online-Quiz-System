from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

import database.db_models as db_models
import models.schemas as schemas
import services.quiz_service as quiz_service
from database.db_connect import get_db
from services.auth import get_current_user
from models.schemas import QuizAttemptCreate, QuizCreate, QuizQuestionMap, QuizScore, QuizAttempt

router = APIRouter(
    prefix="/api/quizzes",
    tags=["quizzes"],
    dependencies=[Depends(get_current_user)]  # Apply auth to all routes
)

@router.get("/", response_model=List[schemas.Quiz], operation_id="list_all_quizzes")
async def get_quizzes(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    return quiz_service.get_all_quizzes(db)

@router.post("/", response_model=schemas.Quiz)
async def create_quiz(
    quiz: schemas.QuizCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    try:
        return quiz_service.create_quiz(db, quiz, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{quiz_id}/questions/", response_model=dict, operation_id="map_quiz_questions")
async def map_questions(
    quiz_id: int,
    question_map: QuizQuestionMap,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    return quiz_service.map_quiz_questions(db, quiz_id, question_map)

@router.get("/user", response_model=List[schemas.Quiz], operation_id="list_user_quizzes")
def read_user_quizzes(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    return quiz_service.get_user_quizzes(db, current_user.id)

@router.get("/{quiz_id}", response_model=schemas.Quiz)
async def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
):
    """Get quiz details - public endpoint, no authentication required"""
    print(f"Processing public access request for quiz {quiz_id}")
    try:
        print(f"Handling get_quiz request for quiz_id: {quiz_id}")
        print(f"Database session valid: {db is not None}")
        
        # Verify database session is active
        if not db or not hasattr(db, 'query'):
            print("Invalid database session")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection error"
            )
        if not quiz_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quiz ID is required"
            )
            
        quiz = quiz_service.get_quiz_by_id(db, quiz_id)
        return quiz
    except ValueError as ve:
        error_msg = str(ve)
        if "not found" in error_msg.lower() or "no questions" in error_msg.lower() or "no valid questions" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting quiz: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the quiz"
        )

@router.post("/{quiz_id}/start/", response_model=schemas.QuizStartResponse)
def start_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    # Get quiz data first
    quiz_data = quiz_service.get_quiz_by_id(db, quiz_id)
    if not quiz_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Start the quiz attempt
    attempt = quiz_service.start_quiz(db, quiz_id, current_user.id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not start quiz"
        )

    # Return both the attempt ID and quiz data
    return {
        "attempt_id": attempt.id,
        "quiz": quiz_data,
    }

@router.post("/{quiz_id}/submit/", response_model=schemas.QuizAttempt, operation_id="submit_quiz_attempt")
async def submit_quiz(
    request: Request,
    quiz_id: int,
    responses: QuizAttemptCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    return quiz_service.submit_quiz(db, quiz_id, current_user.id, responses)

@router.get("/{quiz_id}/participants/", response_model=List[schemas.QuizAttempt], operation_id="list_quiz_participants")
async def get_quiz_participants(
    request: Request,
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    return quiz_service.get_quiz_participants(db, quiz_id)

@router.get("/{quiz_id}/response/", response_model=dict, operation_id="get_quiz_response")
async def get_quiz_response(
    request: Request,
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    return quiz_service.get_quiz_user_response(db, quiz_id, current_user.id)

@router.get("/{quiz_id}/scores/", response_model=List[schemas.QuizScore], operation_id="list_quiz_scores")
async def get_quiz_scores(
    request: Request,
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    from main import limiter  # Import here to avoid circular dependency
    return quiz_service.get_quiz_scores(db, quiz_id)