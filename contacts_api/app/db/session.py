from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from contextlib import contextmanager  # Import contextmanager

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Define get_db as a synchronous context manager
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
