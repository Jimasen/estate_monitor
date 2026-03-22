from datetime import date
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.models.user import User


def check_user_access(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    # Developer override (you)
    if user.is_superuser:
        return {
            "full_access": True,
            "reason": "Developer Override"
        }

    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.is_active == True
    ).first()

    if not subscription:
        return {
            "full_access": False,
            "reason": "No Active Subscription"
        }

    if subscription.end_date < date.today():
        subscription.is_active = False
        db.commit()

        return {
            "full_access": False,
            "reason": "Subscription Expired"
        }

    return {
        "full_access": True,
        "reason": "Active Subscription"
    }
