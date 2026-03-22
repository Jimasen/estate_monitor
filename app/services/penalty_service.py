# app/services/penalty_service.py

from datetime import date
from app.models.late_fee import LateFee
from app.services.status_service import rent_status


DAILY_LATE_FEE_PERCENT = 0.01  # 1% per day


def apply_late_fee(payment, db):
    status_data = rent_status(payment)

    if status_data["status"] != "overdue":
        return

    today = date.today()
    days_overdue = (today - payment.due_date).days

    if days_overdue <= 0:
        return

    penalty_amount = float(payment.amount_due) * DAILY_LATE_FEE_PERCENT

    late_fee = LateFee(
        payment_id=payment.id,
        amount=penalty_amount
    )

    db.add(late_fee)
    db.commit()
