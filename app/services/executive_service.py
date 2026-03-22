from sqlalchemy.orm import Session
from app.models.payment import RentPayment
from sqlalchemy import func

def revenue_summary(db: Session):
    return {
        "total_revenue": db.query(func.sum(RentPayment.amount)).scalar() or 0,
        "paid": db.query(RentPayment).filter(RentPayment.status=="paid").count(),
        "unpaid": db.query(RentPayment).filter(RentPayment.status=="unpaid").count(),
    }
