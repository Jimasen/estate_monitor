# app/api/profile/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User

router = APIRouter()

@router.get("/api/profile")
def profile(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {
        "users": [
            {
                "id": u.id,
                "email": u.email
            }
            for u in users
        ]
    }
