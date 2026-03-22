from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user import UserLogin
from app.services.auth_service import authenticate_user, create_access_token

router = APIRouter()


@router.post("/auth/login")
def login(data: UserLogin, db: Session = Depends(get_db)):

    user = authenticate_user(db, data.email, data.password)

    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
