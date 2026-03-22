# scripts/create_user.py

import logging
from getpass import getpass
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.user import User
from app.models.company import Company   # <-- IMPORTANT
from app.services.auth_service import get_password_hash

# -----------------------------
# Setup logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("create_user")


def main():
    db: Session = SessionLocal()

    try:
        email = input("Enter user email: ").strip()
        password = getpass("Enter password (min 8 chars): ").strip()

        if len(password) < 8:
            logger.error("Password must be at least 8 characters")
            return

        first_name = input("Enter first name (optional): ").strip() or None
        last_name = input("Enter last name (optional): ").strip() or None

        company_id_input = input(
            "Company ID (optional, leave blank for super admin): "
        ).strip()

        company_id = None

        # -----------------------------
        # Validate company foreign key
        # -----------------------------
        if company_id_input:
            company_id = int(company_id_input)

            company = db.query(Company).filter(Company.id == company_id).first()

            if not company:
                logger.error(
                    f"Company with ID {company_id} does not exist. "
                    "Create the company first."
                )
                return

        # -----------------------------
        # Check if user exists
        # -----------------------------
        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user:
            logger.error(f"User {email} already exists")
            return

        # -----------------------------
        # Hash password
        # -----------------------------
        hashed_password = get_password_hash(password)

        # -----------------------------
        # Create user
        # -----------------------------
        user = User(
            email=email,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            company_id=company_id,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(f"✅ User created successfully: {email}")

        if company_id:
            logger.info(f"User assigned to company ID: {company_id}")
        else:
            logger.info("User created as GLOBAL ADMIN (no company)")

    except Exception as e:
        db.rollback()
        logger.exception("Failed to create user: %s", e)

    finally:
        db.close()


if __name__ == "__main__":
    main()
