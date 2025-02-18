from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    quizzes = relationship("Quiz", back_populates="creator")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(String(255), nullable=False)
    options = relationship("QuestionOption", back_populates="question")
    quiz_questions = relationship("QuizQuestion", back_populates="question")
    responses = relationship("QuizResponse", back_populates="question")

class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    option = Column(String(255), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question = relationship("Question", back_populates="options")
    responses = relationship("QuizResponse", back_populates="selected_option")

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200), nullable=False)
    total_questions = Column(Integer, nullable=False)
    total_score = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in minutes
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    questions = relationship("QuizQuestion", back_populates="quiz", lazy="joined")
    attempts = relationship("QuizAttempt", back_populates="quiz")
    creator = relationship("User", back_populates="quizzes")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    question_number = Column(Integer, nullable=False)
    marks = Column(Integer, nullable=False)
    quiz = relationship("Quiz", back_populates="questions", lazy="joined")
    question = relationship("Question", back_populates="quiz_questions", lazy="joined")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, default=datetime.now(timezone.utc))
    end_time = Column(DateTime, nullable=True)
    score = Column(Float, nullable=True)
    status = Column(String(20))  # "in_progress" or "completed"
    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User")
    responses = relationship("QuizResponse", back_populates="attempt")

class QuizResponse(Base):
    __tablename__ = "quiz_responses"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    selected_option_id = Column(Integer, ForeignKey("question_options.id"))
    marks_obtained = Column(Integer, nullable=True, default=0)
    attempt = relationship("QuizAttempt", back_populates="responses")
    question = relationship("Question", back_populates="responses")
    selected_option = relationship("QuestionOption", back_populates="responses")