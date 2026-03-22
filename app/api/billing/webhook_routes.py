# app/api/billing/webhook_routes.py
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
import hashlib
import hmac

from app.database.session import SessionLocal
from app.models.payment import RentPayment
from app.services.payment_processor import process_rent_payment
from app.core.config import settings

router = APIRouter(prefix="/billing/webhooks", tags=["Billing Webhooks"])


# -----------------------------
# PAYSTACK WEBHOOK
# -----------------------------
@router.post("/paystack")
async def paystack_webhook(request: Request):
    secret = settings.PAYSTACK_SECRET_KEY

    if not secret:
        raise HTTPException(status_code=500, detail="Paystack not configured")

    body = await request.body()
    signature = request.headers.get("x-paystack-signature")

    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")

    computed_hash = hmac.new(
        secret.encode(),
        body,
        hashlib.sha512
    ).hexdigest()

    if computed_hash != signature:
        raise HTTPException(status_code=400, detail="Invalid signature")

    payload = await request.json()

    if payload.get("event") == "charge.success":
        reference = payload["data"]["reference"]

        db: Session = SessionLocal()
        payment = db.query(RentPayment).filter(RentPayment.reference == reference).first()

        if payment and payment.status != "paid":
            payment.status = "paid"
            process_rent_payment(db, payment)
            db.commit()

        db.close()

    return {"status": "success"}


# -----------------------------
# FLUTTERWAVE WEBHOOK
# -----------------------------
@router.post("/flutterwave")
async def flutterwave_webhook(request: Request):
    secret = settings.FLUTTERWAVE_SECRET_HASH
    signature = request.headers.get("verif-hash")

    if not secret:
        raise HTTPException(status_code=500, detail="Flutterwave not configured")

    if signature != secret:
        raise HTTPException(status_code=400, detail="Invalid signature")

    body = await request.body()

    if not body:
        return {"status": "ignored", "reason": "empty body"}

    try:
        payload = await request.json()
    except Exception:
        return {"status": "ignored", "reason": "invalid json"}

    if payload.get("event") == "charge.completed":
        reference = payload["data"]["tx_ref"]

        db: Session = SessionLocal()
        payment = db.query(RentPayment).filter(RentPayment.reference == reference).first()

        if payment and payment.status != "paid":
            payment.status = "paid"
            process_rent_payment(db, payment)
            db.commit()

        db.close()

    return {"status": "success"}
