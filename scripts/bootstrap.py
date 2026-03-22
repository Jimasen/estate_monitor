# scripts/bootstrap.py

import logging
from getpass import getpass
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.services.auth_service import get_password_hash

from app.models.user import User
from app.models.company import Company
from app.models.pricing import Pricing


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("bootstrap")


# ----------------------------------
# CREATE SUPER ADMIN
# ----------------------------------
def create_super_admin(db: Session):

    logger.info("Creating Super Admin...")

    email = input("Super Admin Email: ").strip()
    password = getpass("Super Admin Password: ").strip()

    existing = db.query(User).filter(User.email == email).first()

    if existing:
        logger.warning("Super admin already exists")
        return existing

    user = User(
        email=email,
        password=get_password_hash(password),
        first_name="Super",
        last_name="Admin",
        company_id=None,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info("Super Admin created successfully")

    return user


# ----------------------------------
# CREATE DEFAULT COMPANY
# ----------------------------------
def create_default_company(db: Session):

    logger.info("Creating default company...")

    company = db.query(Company).filter(
        Company.email == "demo@estatemonitor.com"
    ).first()

    if company:
        logger.info("Default company already exists")
        return company

    company = Company(
        name="Estate Monitor Demo",
        email="demo@estatemonitor.com",
        phone="+10000000000",
        is_active=True,
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    logger.info("Default company created")

    return company


# ----------------------------------
# CREATE PRICING PLANS
# ----------------------------------
def create_pricing_plans(db: Session):

    logger.info("Creating pricing plans...")

    plans = [
        {
            "name": "Starter",
            "price": 0,
            "description": "Free plan for small landlords managing few properties",
        },
        {
            "name": "Professional",
            "price": 29,
            "description": "Best for property managers managing multiple buildings",
        },
        {
            "name": "Enterprise",
            "price": 99,
            "description": "Advanced SaaS plan for large property organizations",
        },
    ]

    for plan in plans:

        existing = db.query(Pricing).filter(
            Pricing.name == plan["name"]
        ).first()

        if existing:
            logger.info(f"Plan already exists: {plan['name']}")
            continue

        pricing = Pricing(
            name=plan["name"],
            price=plan["price"],
            description=plan["description"],
        )

        db.add(pricing)

    db.commit()

    logger.info("Pricing plans created successfully")


# ----------------------------------
# MAIN BOOTSTRAP
# ----------------------------------
def main():

    db: Session = SessionLocal()

    try:

        logger.info("Starting SaaS bootstrap")

        create_super_admin(db)

        create_default_company(db)

        create_pricing_plans(db)

        logger.info("SaaS bootstrap completed successfully")

    except Exception as e:

        db.rollback()
        logger.exception("Bootstrap failed: %s", e)

    finally:

        db.close()


if __name__ == "__main__":
    main()
