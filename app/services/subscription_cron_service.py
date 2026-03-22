from datetime import date
from sqlalchemy.orm import Session
from app.models.subscription import Subscription


def deactivate_expired_subscriptions(db: Session):
    expired = db.query(Subscription).filter(
        Subscription.is_active == True,
        Subscription.end_date < date.today()
    ).all()

    for sub in expired:
        sub.is_active = False

    db.commit()
