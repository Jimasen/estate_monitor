# scripts/reset_passwords.py

import sys
import os
import logging
import secrets
import string
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User
from app.services.auth_service import get_password_hash


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -----------------------------
# Setup logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("reset_passwords")


def generate_temp_password(length=12):
    """Generate a strong temporary password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    # Truncate if over 72 chars for bcrypt
    return password[:72]


def main():
    db: Session = SessionLocal()
    try:
        email = input("Enter user email to reset password: ").strip()
        user = db.query(User).filter(User.email == email).first()
        if not user:
            logger.error(f"User not found: {email}")
            return

        temp_password = generate_temp_password()
        hashed_password = get_password_hash(temp_password)

        user.password = hashed_password
        db.commit()

        logger.info(f"✅ Password reset successfully for: {email}")
        logger.info(f"Temporary password: {temp_password}")
        print("⚠️ Please communicate this password securely to the user.")

    except Exception as e:
        logger.exception("Failed to reset password: %s", e)
    finally:
        db.close()


if __name__ == "__main__":
    main()
