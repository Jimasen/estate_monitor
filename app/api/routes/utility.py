from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.utility import (
    UtilityBillCreate,
    UtilityBillUpdate,
    UtilityBillOut
)
from app.services.utility_service import (
    create_utility_bill,
    get_utility_bills_by_estate,
    update_utility_bill,
    delete_utility_bill
)

router = APIRouter(prefix="/utilities", tags=["Utility Bills"])


@router.post("/", response_model=UtilityBillOut, status_code=status.HTTP_201_CREATED)
def create_bill(payload: UtilityBillCreate, db: Session = Depends(get_db)): 
    return create_utility_bill(db, payload)


@router.get("/estate/{estate_id}", response_model=List[UtilityBillOut])     
def list_bills(estate_id: int, db: Session = Depends(get_db)):
    return get_utility_bills_by_estate(db, estate_id)


@router.put("/{bill_id}", response_model=UtilityBillOut)
def update_bill(
    bill_id: int,
    payload: UtilityBillUpdate,
    db: Session = Depends(get_db)
):
    bill = update_utility_bill(db, bill_id, payload)
    if not bill:
        raise HTTPException(status_code=404, detail="Utility bill not found")
    return bill


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_bill(bill_id: int, db: Session = Depends(get_db)):
    success = delete_utility_bill(db, bill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Utility bill not found")
