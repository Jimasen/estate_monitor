from sqlalchemy.orm import Session
from app.models.utility import UtilityBill
from app.schemas.utility import UtilityBillCreate, UtilityBillUpdate


def create_utility_bill(db: Session, data: UtilityBillCreate):
    bill = UtilityBill(**data.dict())
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


def get_utility_bills_by_estate(db: Session, estate_id: int):
    return db.query(UtilityBill).filter(
        UtilityBill.estate_id == estate_id
    ).order_by(UtilityBill.due_date.desc()).all()


def update_utility_bill(db: Session, bill_id: int, data: UtilityBillUpdate):
    bill = db.query(UtilityBill).filter(
        UtilityBill.id == bill_id
    ).first()

    if not bill:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(bill, key, value)

    db.commit()
    db.refresh(bill)
    return bill


def delete_utility_bill(db: Session, bill_id: int):
    bill = db.query(UtilityBill).filter(
        UtilityBill.id == bill_id
    ).first()

    if not bill:
        return False

    db.delete(bill)
    db.commit()
    return True
