# app/services/auth_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from app.models.user import User
from app.core.config import settings


# --------------------------------------------------
# Password hashing configuration
# --------------------------------------------------
# Argon2 is modern and secure
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# --------------------------------------------------
# Password hashing
# --------------------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# --------------------------------------------------
# Password verification (safe version)
# --------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # prevents crashes if hash format is invalid
        return False


# --------------------------------------------------
# Authenticate user
# --------------------------------------------------
def authenticate_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return user


# --------------------------------------------------
# Create JWT token
# --------------------------------------------------
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=24)

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return token
