# app/services/subscription_billing_service.py

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.subscription_payment import SubscriptionPayment
from app.models.subscription import Subscription
from app.services.status_service import subscription_status
from app.websocket.status_socket import broadcast_to_tenant


async def activate_subscription(
    db: Session,
    user,
    amount: float,
    plan_name: str = "standard",
    duration_days: int = 30,
):
    """
    Activates or extends a user's subscription
    and broadcasts real-time update to tenant.
    """

    # ----------------------------------------
    # 1️⃣ Record Payment
    # ----------------------------------------
    payment = SubscriptionPayment(
        user_id=user.id,
        amount=amount,
        status="paid",
        paid_at=datetime.utcnow(),
    )

    db.add(payment)

    # ----------------------------------------
    # 2️⃣ Create or Update Subscription
    # ----------------------------------------
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == user.id)
        .first()
    )

    if not subscription:
        subscription = Subscription(user_id=user.id)
        db.add(subscription)

    # Extend from today or existing expiry
    base_date = (
        subscription.expires_at
        if subscription.expires_at and subscription.expires_at > datetime.utcnow()
        else datetime.utcnow()
    )

    subscription.plan = plan_name
    subscription.is_active = True
    subscription.expires_at = base_date + timedelta(days=duration_days)

    # Optional: keep user quick flags in sync
    user.subscription_end = subscription.expires_at.date()
    user.is_active = True

    db.commit()
    db.refresh(subscription)
    db.refresh(user)

    # ----------------------------------------
    # 3️⃣ Get Updated Status
    # ----------------------------------------
    status_data = subscription_status(user)

    # ----------------------------------------
    # 4️⃣ 🔥 Real-Time Tenant Broadcast
    # ----------------------------------------
    await broadcast_to_tenant(
        tenant_id=user.tenant_id,
        message={
            "type": "subscription_status_update",
            "status": status_data.get("status"),
            "plan": subscription.plan,
            "expires_at": subscription.expires_at.isoformat(),
        },
    )

    return subscription
