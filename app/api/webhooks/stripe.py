from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.subscription import Subscription
from datetime import datetime, timedelta
import stripe
import os

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


@router.post("/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Webhook")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_id = int(session["metadata"]["user_id"])

        new_subscription = Subscription(
            user_id=user_id,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
            is_active=True
        )

        db.add(new_subscription)
        db.commit()

    return {"status": "success"}
