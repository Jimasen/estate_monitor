# app/api/admin/dashboard_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.admin_analytics_service import get_admin_metrics, get_estate_metrics
from app.database.session import get_db
from app.core.auth_middleware import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

# -------------------------
# Admin Metrics Endpoint
# -------------------------
@router.get("/metrics")
def admin_metrics(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_admin_metrics(db)

# -------------------------
# Estate Metrics Endpoint
# -------------------------
@router.get("/estate/{estate_id}/metrics")
def estate_metrics(estate_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_estate_metrics(db, estate_id)
