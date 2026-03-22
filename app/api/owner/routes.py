# app/api/owner/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.owner import Owner

router = APIRouter()

@router.get("/api/owner/dashboard")
def owner_dashboard(db: Session = Depends(get_db)):
    owners = db.query(Owner).all()
    return {"owner_count": len(owners)}
