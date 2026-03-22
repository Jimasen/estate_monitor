from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/billing", tags=["Subscriptions"])

@router.post("/subscribe")
def subscribe_user(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Placeholder logic, replace with actual subscription logic
    return {"status": "success", "plan_id": plan_id, "user": current_user.email}
