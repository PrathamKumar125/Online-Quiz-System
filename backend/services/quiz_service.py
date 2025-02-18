from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, text

import database.db_models as db_models
import models.schemas as schemas

def get_all_quizzes(db: Session):
    quizzes = db.query(db_models.Quiz).options(
        joinedload(db_models.Quiz.questions).joinedload(db_models.QuizQuestion.question).joinedload(db_models.Question.options)
    ).all()
    
    # Debug log to verify the data
    for quiz in quizzes:
        if quiz.questions:
            print(f"Quiz {quiz.id} has {len(quiz.questions)} questions")
    return quizzes

def get_quiz_by_id(db: Session, quiz_id: int):
    print(f"Fetching quiz with ID: {quiz_id}")
    
    if not quiz_id:
        raise ValueError("Quiz ID is required")
    
    try:
        print("Attempting database query...")
        print(f"Database connection status: {db.is_active}")
        # Ensure session is fresh
        db.expire_all()
        
        try:
            # Test connection with simple query
            db.execute(text("SELECT 1"))
            print("Database connection test successful")
        except Exception as conn_err:
            print(f"Database connection test failed: {str(conn_err)}")
            raise ValueError(f"Database connection error: {str(conn_err)}")

        quiz = db.query(db_models.Quiz).filter(
            db_models.Quiz.id == quiz_id
        ).options(
            joinedload(db_models.Quiz.questions)
            .joinedload(db_models.QuizQuestion.question)
            .joinedload(db_models.Question.options)
        ).first()
        print("Database query completed successfully")
    except ValueError:
        raise
    except Exception as e:
        print(f"Database error while fetching quiz {quiz_id}: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        raise ValueError(f"Database error: {type(e).__name__} - {str(e)}")
    
    if not quiz:
        print(f"Quiz with ID {quiz_id} not found")
        raise ValueError(f"Quiz with ID {quiz_id} not found")

    # Only validate questions if quiz exists
    if not quiz.questions:
        print(f"Quiz {quiz_id} has no questions")
        raise ValueError(f"Quiz {quiz_id} has no questions")

    # Safely get quiz main attributes with defaults
    transformed_quiz = {
        "id": getattr(quiz, 'id', None),
        "title": getattr(quiz, 'title', ''),
        "duration": getattr(quiz, 'duration', 0),
        "total_questions": getattr(quiz, 'total_questions', 0),
        "total_score": getattr(quiz, 'total_score', 0),
        "creator_id": getattr(quiz, 'creator_id', None),
        "created_at": getattr(quiz, 'created_at', datetime.utcnow()),
        "questions": []
    }

    # Validate required quiz fields
    if not transformed_quiz["id"]:
        raise ValueError(f"Quiz {quiz_id} is missing required field: id")
    if not transformed_quiz["title"]:
        raise ValueError(f"Quiz {quiz_id} is missing required field: title")
    if not transformed_quiz["creator_id"]:
        raise ValueError(f"Quiz {quiz_id} is missing required field: creator_id")
    
    try:
        # Sort questions safely, handling None values
        def get_question_number(x):
            return x.question_number if hasattr(x, 'question_number') and x.question_number is not None else float('inf')
        
        for quiz_question in sorted(quiz.questions, key=get_question_number):
            try:
                if not quiz_question or not quiz_question.question:
                    print(f"Warning: Missing question data for quiz {quiz_id}")
                    continue

                # Safely get question options
                question_options = getattr(quiz_question.question, 'options', [])
                if not question_options:
                    print(f"Warning: No options for question {quiz_question.question.id} in quiz {quiz_id}")
                    continue

                # Safely get question attributes with defaults
                question = quiz_question.question
                question_data = {
                    "id": getattr(question, 'id', None),
                    "text": getattr(question, 'question_text', ''),
                    "marks": getattr(quiz_question, 'marks', 0),
                    "options": []
                }
                
                # Validate required fields
                if not question_data["id"]:
                    print(f"Warning: Missing question ID for quiz {quiz_id}")
                    continue

                # Safely process options
                for option in question_options:
                    if option and hasattr(option, 'id') and hasattr(option, 'option'):
                        question_data["options"].append({
                            "id": option.id,
                            "text": option.option
                        })

                if question_data["options"]:  # Only add questions with valid options
                    transformed_quiz["questions"].append(question_data)
                else:
                    print(f"Warning: No valid options for question {quiz_question.question.id} in quiz {quiz_id}")

            except Exception as e:
                print(f"Error processing question in quiz {quiz_id}: {str(e)}")
                continue
    except Exception as e:
        print(f"Error processing questions for quiz {quiz_id}: {str(e)}")
        raise ValueError(f"Error processing quiz {quiz_id}: {str(e)}")
    
    if not transformed_quiz["questions"]:
        error_msg = f"Quiz {quiz_id} has no valid questions"
        print(f"Warning: {error_msg}")
        raise ValueError(error_msg)

    print(f"Successfully transformed quiz data for ID {quiz_id}")
    return transformed_quiz

def create_quiz(db: Session, quiz: schemas.QuizCreate, creator_id: int):
    db_quiz = db_models.Quiz(
        title=quiz.title,
        creator_id=creator_id,
        total_questions=quiz.total_questions,
        total_score=quiz.total_score,
        duration=quiz.duration,
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def map_quiz_questions(db: Session, quiz_id: int, question_map: schemas.QuizQuestionMap):
    # First remove any existing mappings
    db.query(db_models.QuizQuestion).filter(db_models.QuizQuestion.quiz_id == quiz_id).delete()
    db.flush()
    
    # Add new mappings
    for question in question_map.questions:
        quiz_question = db_models.QuizQuestion(
            quiz_id=quiz_id,
            question_id=question.question_id,
            question_number=question.question_number,
            marks=question.marks
        )
        db.add(quiz_question)
    
    db.commit()
    
    # Fetch and return updated quiz
    quiz = get_quiz_by_id(db, quiz_id)
    return quiz

def get_user_quizzes(db: Session, user_id: int):
    return db.query(db_models.Quiz).filter(db_models.Quiz.creator_id == user_id).all()

def start_quiz(db: Session, quiz_id: int, user_id: int):
    # Create new attempt
    attempt = db_models.QuizAttempt(
        quiz_id=quiz_id,
        user_id=user_id,
        status="in_progress"
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt

def submit_quiz(db: Session, quiz_id: int, user_id: int, responses: schemas.QuizAttemptCreate):
    # Get the most recent attempt for this quiz by this user
    attempt = db.query(db_models.QuizAttempt).filter(
        db_models.QuizAttempt.quiz_id == quiz_id,
        db_models.QuizAttempt.user_id == user_id,
        db_models.QuizAttempt.status == "in_progress"
    ).order_by(db_models.QuizAttempt.start_time.desc()).first()
    
    if not attempt:
        return None
    
    score = 0
    total_questions = len(responses.responses)
    
    # Record responses
    for response in responses.responses:
        # Check if the selected option is correct and get marks
        question = db.query(db_models.Question).get(response.question_id)
        marks = 0
        if question:
            correct_option = next((opt for opt in question.options if opt.id == response.selected_option_id and opt.is_correct), None)
            if correct_option:
                marks = 1  # Or any other scoring logic
                score += marks

        quiz_response = db_models.QuizResponse(
            attempt_id=attempt.id,
            question_id=response.question_id,
            selected_option_id=response.selected_option_id,
            marks_obtained=marks
        )
        db.add(quiz_response)
    
    # Update attempt status and score
    attempt.status = "completed"
    attempt.end_time = datetime.now()
    attempt.score = (score / total_questions * 100) if total_questions > 0 else 0
    
    db.commit()
    db.refresh(attempt)
    return attempt

def get_quiz_participants(db: Session, quiz_id: int):
    attempts = db.query(db_models.QuizAttempt).filter(
        db_models.QuizAttempt.quiz_id == quiz_id
    ).all()
    return attempts

def get_quiz_user_response(db: Session, quiz_id: int, user_id: int):
    # Get the most recent attempt for this quiz by this user
    attempt = db.query(db_models.QuizAttempt).filter(
        db_models.QuizAttempt.quiz_id == quiz_id,
        db_models.QuizAttempt.user_id == user_id
    ).order_by(db_models.QuizAttempt.start_time.desc()).first()
    
    if not attempt:
        return None
    
    responses = []
    for response in attempt.responses:
        responses.append({
            "question_id": response.question_id,
            "selected_option_id": response.selected_option_id
        })
    
    return {
        "attempt_id": attempt.id,
        "start_time": attempt.start_time,
        "end_time": attempt.end_time,
        "status": attempt.status,
        "responses": responses
    }

def get_quiz_scores(db: Session, quiz_id: int):
    # Get all attempts for this quiz
    attempts = db.query(db_models.QuizAttempt).filter(
        db_models.QuizAttempt.quiz_id == quiz_id,
        db_models.QuizAttempt.end_time.isnot(None)  # Only get completed attempts
    ).all()
    
    scores = []
    for attempt in attempts:
        # Calculate number of correct answers (where marks_obtained > 0)
        correct_answers = db.query(func.count(db_models.QuizResponse.id)).filter(
            db_models.QuizResponse.attempt_id == attempt.id,
            db_models.QuizResponse.marks_obtained > 0
        ).scalar()
        
        total_questions = db.query(func.count(db_models.QuizResponse.id)).filter(
            db_models.QuizResponse.attempt_id == attempt.id
        ).scalar()
        
        scores.append({
            "user_id": attempt.user_id,
            "score": attempt.score,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "completion_time": attempt.end_time.isoformat() if attempt.end_time else None
        })
    
    return scores