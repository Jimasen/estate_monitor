# app/api/auth/register_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.user import User
from app.database.session import get_db
from app.services.auth_service import hash_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str

@router.post("/register")
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(data.password)

    names = data.full_name.strip().split(" ", 1)
    first_name = names[0]
    last_name = names[1] if len(names) > 1 else ""

    new_user = User(
        email=data.email,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email, "id": new_user.id})

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "access_token": token,
        "token_type": "bearer"
    }
