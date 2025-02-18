from sqlalchemy.orm import Session
from database.db_connect import engine, SessionLocal
from database.db_models import Base, User
from services.auth import get_password_hash

def init_db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if test user exists
        user = db.query(User).filter(User.username == "admin").first()
        if not user:
            # Create test user
            test_user = User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                is_admin=True
            )
            db.add(test_user)
            db.commit()
            print("Created test user 'admin' with password 'admin123'")
        else:
            print("Test user already exists")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()