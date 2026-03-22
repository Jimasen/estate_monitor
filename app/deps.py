# app/deps.py
from sqlalchemy.orm import Session
from app.database.session import SessionLocal

def get_db():
    """
    Provides a database session for requests.
    Use as: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
