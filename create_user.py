# reset_passwords.py
import os
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

# Initialize bcrypt password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Max length bcrypt can handle
MAX_BCRYPT_LENGTH = 72

def hash_password(password: str) -> str:
    """Ensure password is <=72 chars and hashed."""
    trimmed = password[:MAX_BCRYPT_LENGTH]
    return pwd_context.hash(trimmed)

def reset_user_passwords():
    db: Session = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            if len(user.password) > MAX_BCRYPT_LENGTH or not user.password.startswith("$2b$"):
                # If the stored password is plain text or too long, re-hash
                print(f"Resetting password for: {user.email}")
                # For demo/testing: assign a default secure temporary password
                temp_password = "TempPass1234!"[:MAX_BCRYPT_LENGTH]
                user.password = hash_password(temp_password)
        db.commit()
        print("✅ Password reset completed.")
    finally:
        db.close()

if __name__ == "__main__":
    reset_user_passwords()
