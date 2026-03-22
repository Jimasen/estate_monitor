# app/api/payments/flutterwave_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.auth.deps import get_current_user
from app.models.user import User
from app.services.payment_gateway import init_payment_gateway, confirm_payment

import uuid

router = APIRouter(prefix="/api/payments/flutterwave", tags=["Flutterwave"])

@router.post("/init")
def init_flutterwave_payment(amount: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reference = str(uuid.uuid4())
    payment_link = init_payment_gateway(
        payment=type('Temp', (), {"amount_due": amount, "tenant": current_user, "id": reference})(),
        platform="flutterwave"
    )

    if not payment_link:
        raise HTTPException(status_code=400, detail="Payment init failed")

    return {"payment_url": payment_link, "reference": reference}

@router.post("/verify")
def verify_flutterwave_payment(reference: str, db: Session = Depends(get_db)):
    # Normally you would fetch amount from Flutterwave API
    amount_from_api = 0  # Replace with actual API call
    payment = confirm_payment(payment_id=reference, amount_paid=amount_from_api)
    return {"status": "success", "payment": payment.id}
