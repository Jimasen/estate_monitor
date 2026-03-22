# app/api/admin/user_routes.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.user import User
from app.database.session import get_db
from app.core.auth_middleware import get_current_admin_user  # admin-only dependency

router = APIRouter(
    prefix="/admin/users",
    tags=["Admin Users"]
)

# --- Soft Delete Endpoint ---
@router.patch("/{user_id}/soft-delete")
def soft_delete_user(
    user_id: int,
    confirm: bool = Query(False, description="Must be true to actually soft delete the user"),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin_user)
):
    """
    Soft-delete a user (admin only). Requires confirmation via '?confirm=true'.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")    

    if user.is_deleted:
        raise HTTPException(status_code=400, detail="User already deleted")

    if not confirm:
        raise HTTPException(
            status_code=400,
            detail=f"Deletion not confirmed. Add '?confirm=true' to confirm soft deleting user '{user.email}'."
        )

    user.is_deleted = True
    user.is_active = False
    user.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return {"message": f"User '{user.email}' soft deleted successfully."}


# --- Restore Endpoint ---
@router.patch("/{user_id}/restore")
def restore_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin_user)
):
    """
    Restore a previously soft-deleted user (admin only).
    """
    user = db.query(User).filter(User.id == user_id, User.is_deleted == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not deleted")

    user.is_deleted = False
    user.is_active = True
    user.deleted_at = None

    db.commit()
    db.refresh(user)

    return {"message": f"User '{user.email}' restored successfully."}
