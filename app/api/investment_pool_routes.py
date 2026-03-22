from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.investment import Investment

router = APIRouter(prefix="/investment-pool", tags=["Investment Pool"])


@router.get("/")
def list_investments(db: Session = Depends(get_db)):
    return db.query(Investment).all()


@router.post("/join")
def join_investment(investment_id: int, amount: float, db: Session = Depends(get_db)):
    inv = db.query(Investment).filter(Investment.id == investment_id).first()
    if not inv:
        return {"error": "Investment not found"}

    inv.amount_raised += amount
    db.commit()

    return {"status": "investment added"}

