# app/services/risk_analysis_service.py

from sqlalchemy.orm import Session
from datetime import datetime

from app.models.tenant import Tenant
from app.models.payment import RentPayment


def calculate_tenant_risk(db: Session, tenant: Tenant):

    payments = (
        db.query(RentPayment)
        .filter(RentPayment.tenant_id == tenant.id)
        .order_by(RentPayment.due_date.desc())
        .limit(6)
        .all()
    )

    if not payments:
        return 0

    late_count = 0
    total = len(payments)

    for payment in payments:

        if payment.paid_at and payment.paid_at > payment.due_date:
            late_count += 1

        if payment.status == "pending" and payment.due_date < datetime.utcnow():
            late_count += 1

    risk_score = late_count / total

    tenant.risk_score = risk_score

    db.commit()

    return risk_score
