from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class User(UserBase):
    id: int
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class QuestionOptionBase(BaseModel):
    option_text: str
    is_correct: bool

class QuestionOption(QuestionOptionBase):
    id: int  # UNSIGNED INT

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    question_text: str

class QuestionCreate(QuestionBase):
    options: List[QuestionOptionBase]

class Question(QuestionBase):
    id: int  # UNSIGNED INT
    options: List[QuestionOption]

    class Config:
        from_attributes = True
        
class QuizQuestionBase(BaseModel):
    question_number: int
    marks: int

class QuizQuestion(QuizQuestionBase):
    id: int
    quiz_id: int
    question_id: int
    question: Question

    class Config:
        from_attributes = True

class QuizBase(BaseModel):
    title: str
    total_questions: int
    total_score: int
    duration: int

class QuizCreate(QuizBase):
    pass

class Quiz(QuizBase):
    id: int
    creator_id: int
    created_at: datetime
    questions: List[QuizQuestion]

    class Config:
        from_attributes = True

class QuizQuestionCreate(BaseModel):
    question_id: int
    question_number: int
    marks: int

class QuizQuestionMap(BaseModel):
    quiz_id: int
    questions: List[QuizQuestionCreate]

class QuizResponse(BaseModel):
    question_id: int
    selected_option_id: int
    marks_obtained: int = 0

    class Config:
        from_attributes = True

class QuizScore(BaseModel):
    user_id: int
    score: float
    correct_answers: int
    total_questions: int
    completion_time: str | None

    class Config:
        from_attributes = True

class QuizAttemptCreate(BaseModel):
    responses: List[QuizResponse]

class QuizAttempt(BaseModel):
    id: int
    quiz_id: int
    user_id: int
    start_time: datetime
    end_time: datetime | None
    score: float | None
    status: str
    responses: List[QuizResponse]

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class QuizStartResponse(BaseModel):
    attempt_id: int
    quiz: dict  # This will contain all quiz data including questions