# app/services/payment_status_service.py

from datetime import date
from app.models.payment import RentPayment


def get_payment_status_indicator(payment: RentPayment) -> str:
    """
    Returns:
        paid
        ready
        overdue
    Used for Flutter radio light indicator.
    """

    today = date.today()

    if payment.status == "paid":
        return "paid"

    if payment.due_date and payment.due_date < today:
        return "overdue"

    return "ready"
