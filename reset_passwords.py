import os
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_LENGTH = 72

def hash_password(password: str) -> str:
    trimmed = password[:MAX_BCRYPT_LENGTH]
    return pwd_context.hash(trimmed)

def reset_user_passwords():
    db: Session = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            if len(user.password) > MAX_BCRYPT_LENGTH or not user.password.startswith("$2b$"):
                print(f"Resetting password for: {user.email}")
                temp_password = "TempPass1234!"[:MAX_BCRYPT_LENGTH]
                user.password = hash_password(temp_password)
        db.commit()
        print("✅ Password reset completed.")
    finally:
        db.close()

if __name__ == "__main__":
    reset_user_passwords()
