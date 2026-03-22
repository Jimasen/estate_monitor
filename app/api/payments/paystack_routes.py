from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import os
import requests

from app.database.session import get_db
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/paystack", tags=["Paystack Payments"])

@router.post("/init")
def init_paystack_payment(
    amount: float,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    paystack_secret = os.getenv("PAYSTACK_SECRET_KEY")
    if not paystack_secret:
        raise HTTPException(status_code=500, detail="Paystack not configured")

    payload = {
        "email": current_user.email,
        "amount": int(amount * 100),  # kobo
        "callback_url": str(request.base_url) + "payments/paystack/callback",
    }

    headers = {
        "Authorization": f"Bearer {paystack_secret}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        json=payload,
        headers=headers,
        timeout=30,
    )

    data = response.json()

    if not data.get("status"):
        raise HTTPException(status_code=400, detail=data.get("message"))

    return {
        "authorization_url": data["data"]["authorization_url"],
        "reference": data["data"]["reference"],
    }
