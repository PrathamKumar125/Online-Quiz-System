from dotenv import load_dotenv
import os

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/sparki_cms"
)

print(f"Initializing database connection to: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=5,         # Set reasonable pool size
    max_overflow=10,     # Allow some overflow connections
    pool_timeout=30,     # Set connection timeout
    pool_recycle=1800,   # Recycle connections after 30 minutes
    echo=True           # Log SQL queries for debugging
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        # Clear any stale state
        db.rollback()
        
        # Verify connection is working
        db.execute(text("SELECT 1"))
        
        yield db
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        # Ensure session is rolled back on error
        try:
            db.rollback()
        except Exception:
            pass
        raise
    finally:
        try:
            db.close()
        except Exception as e:
            print(f"Error closing database connection: {str(e)}")
        finally:
            del db  # Ensure session is fully cleaned up