# app/api/dashboard/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from .overview import router as overview_router
from app.database.session import get_db
from app.models.tenant import Tenant
from app.models.property import Property
from app.models.payment import RentPayment

router = APIRouter()

# include overview routes
router.include_router(overview_router)


# ================================
# DASHBOARD ANALYTICS (RESTORED)
# ================================
@router.get("/dashboard/analytics")
def dashboard_analytics(db: Session = Depends(get_db)):

    today = date.today()

    total_tenants = db.query(func.count(Tenant.id)).scalar()
    total_properties = db.query(func.count(Property.id)).scalar()

    monthly_revenue = db.query(func.sum(RentPayment.amount)).filter(
        func.extract('month', RentPayment.paid_at) == today.month,
        func.extract('year', RentPayment.paid_at) == today.year,
        RentPayment.status == "paid"
    ).scalar() or 0

    late_rent_count = db.query(Tenant).filter(
        Tenant.rent_due_date < today
    ).count()

    return {
        "total_tenants": total_tenants,
        "total_properties": total_properties,
        "monthly_revenue": monthly_revenue,
        "late_rent_count": late_rent_count
    }


# ================================
# DASHBOARD ACTIVITY + ANALYTICS
# ================================
@router.get("/dashboard/activity")
def dashboard_activity(db: Session = Depends(get_db)):

    today = date.today()

    # ----------------------------
    # RECENT DATA
    # ----------------------------
    recent_tenants = db.query(Tenant).order_by(Tenant.id.desc()).limit(5).all()
    recent_payments = db.query(RentPayment).order_by(RentPayment.id.desc()).limit(5).all()

    # ----------------------------
    # ANALYTICS
    # ----------------------------
    total_tenants = db.query(func.count(Tenant.id)).scalar()
    total_properties = db.query(func.count(Property.id)).scalar()

    monthly_revenue = db.query(func.sum(RentPayment.amount)).filter(
        func.extract('month', RentPayment.paid_at) == today.month,
        func.extract('year', RentPayment.paid_at) == today.year,
        RentPayment.status == "paid"
    ).scalar() or 0

    late_rent_count = db.query(Tenant).filter(
        Tenant.rent_due_date < today
    ).count()

    late_payments_count = db.query(RentPayment).filter(
        RentPayment.due_date < today,
        RentPayment.status != "paid"
    ).count()

    # ----------------------------
    # RESPONSE
    # ----------------------------
    return {
        "analytics": {
            "total_tenants": total_tenants,
            "total_properties": total_properties,
            "monthly_revenue": monthly_revenue,
            "late_rent_count": late_rent_count,
            "late_payments_count": late_payments_count
        },
        "recent_tenants": [
            {
                "id": t.id,
                "name": t.full_name,
                "phone": t.phone,
                "property": t.property.name if t.property else None
            }
            for t in recent_tenants
        ],
        "recent_payments": [
            {
                "id": p.id,
                "amount": p.amount,
                "status": p.status,
                "due_date": p.due_date,
                "paid_at": p.paid_at,
                "reference": p.reference,
                "gateway": p.gateway,
                "tenant_name": p.tenant.full_name if p.tenant else None,
                "tenant_phone": p.tenant.phone if p.tenant else None,
                "property_name": p.tenant.property.name if p.tenant and p.tenant.property else None
            }
            for p in recent_payments
        ]
    }
