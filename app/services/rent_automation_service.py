# app/services/rent_automation_service.py

import logging
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.tenant import Tenant
from app.core.events import emit, RENT_DUE

logger = logging.getLogger("rent_automation")


# --------------------------------------------------
# RENT REMINDER ENGINE
# --------------------------------------------------
def process_rent_reminders(db: Session):

    today = datetime.utcnow().date()

    tenants = db.query(Tenant).all()

    for tenant in tenants:

        if not tenant.rent_due_date:
            continue

        due_date = tenant.rent_due_date.date()

        days_remaining = (due_date - today).days

        try:

            if days_remaining in [7, 3, 1]:

                emit(RENT_DUE, {"tenant": tenant})

        except Exception as e:
            logger.exception(f"Reminder processing failed: {e}")


# --------------------------------------------------
# LATE PAYMENT DETECTOR
# --------------------------------------------------
def process_late_payments(db: Session):

    today = datetime.utcnow().date()

    tenants = db.query(Tenant).all()

    for tenant in tenants:

        if not tenant.rent_due_date:
            continue

        due_date = tenant.rent_due_date.date()

        if today > due_date:

            days_late = (today - due_date).days

            logger.info(f"Tenant {tenant.id} is {days_late} days late")

            if days_late == 1:
                emit("rent_late", {"tenant": tenant})

            if days_late >= 7:
                emit("rent_critical", {"tenant": tenant})
