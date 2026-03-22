# app/services/risk_scoring_service.py

import logging
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.tenant import Tenant

logger = logging.getLogger("risk_scoring")


def calculate_tenant_risk(db: Session, tenant_id: int):

    tenant = db.query(Tenant).get(tenant_id)

    if not tenant:
        return None

    payments = db.query(Payment).filter(
        Payment.tenant_id == tenant_id
    ).all()

    score = 0

    for p in payments:

        if p.status == "late":
            score += 15

        if p.status == "failed":
            score += 25

        if p.status == "missed":
            score += 35

    if score < 30:
        risk = "LOW"

    elif score < 60:
        risk = "MEDIUM"

    elif score < 80:
        risk = "HIGH"

    else:
        risk = "DEFAULTER"

    tenant.risk_score = score
    tenant.risk_level = risk

    db.commit()

    logger.info(f"Tenant {tenant_id} risk updated → {risk}")

    return risk
