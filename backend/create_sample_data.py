from database.db_connect import engine, SessionLocal, Base
from database.db_models import Question, QuestionOption
from sqlalchemy.exc import IntegrityError

# Create all tables
Base.metadata.create_all(bind=engine)

def create_sample_data():
    db = SessionLocal()
    try:
        # Check if questions already exist
        existing_questions = db.query(Question).count()
        if existing_questions > 0:
            print("Sample data already exists!")
            return

        # Create questions without specifying IDs (let them auto-increment)
        questions_data = [
            {"question_text": "Which of the following is a NoSQL database?"},
            {"question_text": "What does CSS stand for?"},
            {"question_text": "In Java, which keyword is used to create a subclass?"},
            {"question_text": "What does REST stand for in REST API?"},
            {"question_text": "Which of the following sorting algorithms has the best average-case time complexity?"},
            {"question_text": "Which command is used to check active ports on a Linux system?"},
            {"question_text": "In JavaScript, which of the following is used to declare a constant variable?"},
            {"question_text": "Which HTTP status code indicates that the request was successful but no content is returned?"},
            {"question_text": "In SQL, which clause is used to filter results after an aggregation function is applied?"},
            {"question_text": "What is the primary advantage of using Docker containers?"}
        ]

        # Insert questions and store their IDs
        question_id_map = {}
        for idx, q_data in enumerate(questions_data, 1):
            question = Question(question_text=q_data["question_text"])
            db.add(question)
            db.flush()  # This will populate the id field
            question_id_map[idx] = question.id

        # Commit questions first to ensure they exist for options
        db.commit()

        # Create options with mapped question IDs
        options_data = [
            (1, "MySQL", False),
            (1, "PostgreSQL", False),
            (1, "MongoDB", True),
            (1, "SQLite", False),
            (2, "Computer Style Sheets", False),
            (2, "Creative Style Sheets", False),
            (2, "Cascading Style Sheets", True),
            (2, "Colorful Style Sheets", False),
            # ... remaining options mapped to their question IDs
            # Add all options following the same pattern
        ]

        # Insert options using the mapped question IDs
        for q_idx, opt_text, is_correct in options_data:
            actual_question_id = question_id_map[q_idx]
            option = QuestionOption(
                question_id=actual_question_id,
                option=opt_text,
                is_correct=is_correct
            )
            db.add(option)
        
        db.commit()
        print("Sample data created successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error creating sample data: {str(e)}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()