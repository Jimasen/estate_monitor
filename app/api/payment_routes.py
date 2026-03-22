# app/api/payment_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database.session import get_db
from app.models.payment import Payment  # assuming you have a Payment model
from app.models.user import User

router = APIRouter()

# =========================
# Request & Response Schemas
# =========================
class PaymentRequest(BaseModel):
    amount: float

class PaymentResponse(BaseModel):
    id: int
    amount: float
    user_id: int
    created_at: str

# =========================
# GET all payments
# =========================
@router.get("/api/pay", response_model=List[PaymentResponse])
def get_payments(db: Session = Depends(get_db)):
    payments = db.query(Payment).all()
    return payments

# =========================
# POST /api/pay
# =========================
@router.post("/api/pay", response_model=PaymentResponse)
def create_payment(data: PaymentRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    payment = Payment(
        amount=data.amount,
        user_id=current_user.id
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment
