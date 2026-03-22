# app/api/payment/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/pay")

@router.get("/")
def list_payments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # now only logged-in users can access
    return {"message": f"Hello {current_user.email}, you can see payments!"}

@router.post("/")
def create_payment(amount: float, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # logic to create payment
    return {"message": f"Payment of {amount} created for {current_user.email}"}
