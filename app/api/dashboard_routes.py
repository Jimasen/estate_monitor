from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.payment import RentPayment
from app.models.subscription import Subscription
from app.services.payment_status_service import get_payment_status_indicator

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/payment-status")
def get_payment_status(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Returns rent and subscription indicator for dashboard radio lights.
    """

    # ---- RENT STATUS ----
    payment = (
        db.query(RentPayment)
        .filter(RentPayment.tenant_id == user.id)
        .order_by(RentPayment.due_date.desc())
        .first()
    )

    rent_status = "no_activity"
    if payment:
        rent_status = get_payment_status_indicator(payment)

    # ---- SUBSCRIPTION STATUS ----
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == user.id)
        .order_by(Subscription.end_date.desc())
        .first()
    )

    subscription_status = "no_activity"

    if subscription:
        if subscription.is_active:
            if subscription.end_date and subscription.end_date < date.today():
                subscription_status = "overdue"
            else:
                subscription_status = "paid"
        else:
            subscription_status = "overdue"

    return {
        "rent_status": rent_status,
        "subscription_status": subscription_status
    }
