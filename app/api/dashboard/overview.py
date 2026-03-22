from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.session import get_db
from app.models.tenant import Tenant
from app.models.property import Property
from app.models.payment import Payment

router = APIRouter()

@router.get("/dashboard/overview")
def dashboard_overview(db: Session = Depends(get_db)):

    tenants = db.query(func.count(Tenant.id)).scalar()
    properties = db.query(func.count(Property.id)).scalar()
    revenue = db.query(func.sum(Payment.amount)).scalar() or 0

    return {
        "tenants": tenants,
        "properties": properties,
        "revenue": revenue
    }
