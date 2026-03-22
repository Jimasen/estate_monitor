from fastapi import Request, HTTPException, status
from app.database.session import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()

    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return user

def set_session(request: Request, user: User):
    request.session.clear()
    request.session["user_id"] = user.id
    request.session["role"] = user.role
    request.session["tenant_id"] = user.tenant_id

def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    db = SessionLocal()
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    return user
