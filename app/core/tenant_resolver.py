# app/core/tenant_resolver.py

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.company import Company


def get_tenant_db(domain: str):
    """
    Resolve tenant company from request domain
    """
    db: Session = SessionLocal()

    try:
        company = db.query(Company).filter(Company.domain == domain).first()
        return company
    finally:
        db.close()
