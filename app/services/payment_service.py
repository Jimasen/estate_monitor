from sqlalchemy.orm import Session
from datetime import datetime
from app.models.subscription_payment import SubscriptionPayment
from app.services.gateway_router import create_payment_reference
from app.services.payment_gateway import ledger_service


def auto_charge_subscription(db: Session, frequency: str):
    from app.models import User

    users = db.query(User).filter(
        User.subscription_active == True,
        User.subscription_frequency == frequency
    ).yield_per(100)

    for user in users:
        existing_payment = db.query(SubscriptionPayment).filter(
            SubscriptionPayment.user_id == user.id,
            SubscriptionPayment.status == "pending",
            SubscriptionPayment.billing_cycle == frequency
        ).first()

        if existing_payment:
            continue

        amount = 5000 if frequency=="monthly" and user.subscription_plan=="basic" else \
                 50000 if frequency=="annual" and user.subscription_plan=="basic" else \
                 10000 if frequency=="monthly" and user.subscription_plan=="pro" else \
                 100000 if frequency=="annual" and user.subscription_plan=="pro" else 0

        if amount == 0:
            continue

        payment = SubscriptionPayment(
            user_id=user.id,
            amount=amount,
            billing_cycle=frequency,
            status="pending",
            created_at=datetime.utcnow()
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        try:
            # Create actual payment reference
            create_payment_reference(payment)

            # Ledger entry: 1% platform fee
            fee_amount = amount * 0.01
            ledger_service.credit_platform_fee(user.id, fee_amount, payment.id)

        except Exception as e:
            print(f"⚠ Gateway failed for user {user.id}: {e}")
