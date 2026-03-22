# app/api/admin/admin_analytics_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.admin_analytics_service import (
    get_admin_metrics,
    get_estate_metrics,
    get_monthly_revenue_chart
)
from app.core.auth_middleware import get_current_user
from app.database.session import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# -------------------------
# Admin Metrics
# -------------------------
@router.get("/admin-metrics")
def admin_metrics(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_admin_metrics(db)

# -------------------------
# Estate Metrics
# -------------------------
@router.get("/estate-metrics/{estate_id}")
def estate_metrics(estate_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_estate_metrics(db, estate_id)

# -------------------------
# Monthly Revenue Chart
# -------------------------
@router.get("/monthly-revenue")
def monthly_revenue(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_monthly_revenue_chart(db)
