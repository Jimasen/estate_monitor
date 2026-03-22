from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.subscription import Subscription
from datetime import datetime, timedelta
import hmac
import hashlib
import os

router = APIRouter()


@router.post("/paystack")
async def paystack_webhook(request: Request, db: Session = Depends(get_db)):

    payload = await request.body()
    signature = request.headers.get("x-paystack-signature")

    secret = os.getenv("PAYSTACK_SECRET_KEY")

    computed_hash = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha512
    ).hexdigest()

    if computed_hash != signature:
        raise HTTPException(status_code=400, detail="Invalid Signature")

    data = await request.json()

    if data["event"] == "charge.success":

        user_id = int(data["data"]["metadata"]["user_id"])

        new_subscription = Subscription(
            user_id=user_id,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
            is_active=True
        )

        db.add(new_subscription)
        db.commit()

    return {"status": "success"}
