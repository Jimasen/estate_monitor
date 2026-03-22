# app/dependencies/auth.py
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Return the current logged-in user based on session.
    Raises 401 if user not found.
    """
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user
