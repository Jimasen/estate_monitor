# app/services/admin_analytics_service.py

from sqlalchemy import func, and_, extract
from sqlalchemy.orm import Session
from datetime import date

from app.models.payment import Payment
from app.models.user import User
from app.models.subscription import Subscription
from app.models.tenant import Tenant
from app.models.late_fee import LateFee
from app.services.risk_scoring_service import calculate_tenant_risk

# ==========================================================
# GLOBAL ADMIN METRICS (Platform-Level)
# ==========================================================
def get_admin_metrics(db: Session):
    today = date.today()
    
    # USERS
    total_users = db.query(func.count(User.id)).scalar() or 0
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0
    suspended_users = db.query(func.count(User.id)).filter(User.is_active == False).scalar() or 0
    active_subscriptions = db.query(func.count(Subscription.id)).filter(Subscription.is_active == True).scalar() or 0
    total_tenants = db.query(func.count(Tenant.id)).scalar() or 0

    # REVENUE
    total_revenue = db.query(func.sum(RentPayment.amount_due)).filter(RentPayment.status == "paid").scalar() or 0
    monthly_revenue = db.query(func.sum(RentPayment.amount_due)).filter(
        and_(
            RentPayment.status == "paid",
            extract("month", RentPayment.due_date) == today.month,
            extract("year", RentPayment.due_date) == today.year
        )
    ).scalar() or 0

    # OVERDUE
    overdue_rents_count = db.query(func.count(RentPayment.id)).filter(
        and_(RentPayment.status == "pending", RentPayment.due_date < today)
    ).scalar() or 0
    overdue_revenue = db.query(func.sum(RentPayment.amount_due)).filter(
        and_(RentPayment.status == "pending", RentPayment.due_date < today)
    ).scalar() or 0

    # LATE FEES
    late_fee_revenue = db.query(func.sum(LateFee.amount)).filter(LateFee.is_paid == True).scalar() or 0

    # COLLECTION RATE %
    total_expected = db.query(func.sum(RentPayment.amount_due)).scalar() or 0
    collection_rate = (float(total_revenue) / float(total_expected) * 100) if total_expected > 0 else 0.0

    # PLATFORM RISK SCORE
    tenants = db.query(Tenant).all()
    risk_scores = [calculate_tenant_risk(t) for t in tenants]
    average_risk_score = (sum(risk_scores) / len(risk_scores)) if risk_scores else 0.0

    return {
        "total_users": total_users,
        "active_users": active_users,
        "suspended_users": suspended_users,
        "active_subscriptions": active_subscriptions,
        "total_tenants": total_tenants,
        "total_revenue": float(total_revenue),
        "monthly_revenue": float(monthly_revenue),
        "overdue_rents_count": overdue_rents_count,
        "overdue_revenue": float(overdue_revenue),
        "late_fee_revenue": float(late_fee_revenue),
        "collection_rate_percent": round(collection_rate, 2),
        "average_risk_score": round(average_risk_score, 2)
    }

# ==========================================================
# ESTATE-SPECIFIC METRICS
# ==========================================================
def get_estate_metrics(db: Session, estate_id: int):
    today = date.today()

    total_revenue = db.query(func.sum(RentPayment.amount_due)).filter(
        and_(RentPayment.status == "paid", RentPayment.estate_id == estate_id)
    ).scalar() or 0

    monthly_revenue = db.query(func.sum(RentPayment.amount_due)).filter(
        and_(
            RentPayment.status == "paid",
            RentPayment.estate_id == estate_id,
            extract("month", RentPayment.due_date) == today.month,
            extract("year", RentPayment.due_date) == today.year
        )
    ).scalar() or 0

    overdue_rents_count = db.query(func.count(RentPayment.id)).filter(
        and_(RentPayment.status == "pending", RentPayment.estate_id == estate_id, RentPayment.due_date < today)
    ).scalar() or 0

    overdue_revenue = db.query(func.sum(RentPayment.amount_due)).filter(
        and_(RentPayment.status == "pending", RentPayment.estate_id == estate_id, RentPayment.due_date < today)
    ).scalar() or 0

    late_fee_revenue = db.query(func.sum(LateFee.amount)).join(
        RentPayment, LateFee.payment_id == RentPayment.id
    ).filter(and_(RentPayment.estate_id == estate_id, LateFee.is_paid == True)).scalar() or 0

    active_tenants = db.query(func.count(Tenant.id)).filter(
        and_(Tenant.estate_id == estate_id, Tenant.is_active == True)
    ).scalar() or 0
    suspended_tenants = db.query(func.count(Tenant.id)).filter(
        and_(Tenant.estate_id == estate_id, Tenant.is_active == False)
    ).scalar() or 0

    total_expected = db.query(func.sum(RentPayment.amount_due)).filter(RentPayment.estate_id == estate_id).scalar() or 0
    collection_rate = (float(total_revenue) / float(total_expected) * 100) if total_expected > 0 else 0.0

    tenants = db.query(Tenant).filter(Tenant.estate_id == estate_id).all()
    risk_scores = [calculate_tenant_risk(t) for t in tenants]
    average_risk_score = (sum(risk_scores) / len(risk_scores)) if risk_scores else 0.0

    return {
        "estate_id": estate_id,
        "total_revenue": float(total_revenue),
        "monthly_revenue": float(monthly_revenue),
        "overdue_rents_count": overdue_rents_count,
        "overdue_revenue": float(overdue_revenue),
        "late_fee_revenue": float(late_fee_revenue),
        "active_tenants": active_tenants,
        "suspended_tenants": suspended_tenants,
        "collection_rate_percent": round(collection_rate, 2),
        "average_risk_score": round(average_risk_score, 2)
    }

# ==========================================================
# MONTHLY REVENUE CHART
# ==========================================================
def get_monthly_revenue_chart(db: Session):
    today = date.today()
    current_year = today.year

    results = db.query(
        extract("month", RentPayment.due_date).label("month"),
        func.sum(RentPayment.amount_due)
    ).filter(RentPayment.status == "paid", extract("year", RentPayment.due_date) == current_year
    ).group_by("month").all()

    month_map = {int(month): float(amount) for month, amount in results}
    return [{"month": m, "revenue": month_map.get(m, 0.0)} for m in range(1, 13)]
