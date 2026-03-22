from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.session import get_db
from app.models.audit import TenantComment
from app.services.ws_manager import manager

router = APIRouter(
    prefix="/api/estate",
    tags=["Estate Admin"]
)

# -----------------------------
# LIST TENANT COMMENTS
# -----------------------------
@router.get("/admin/comments")
def list_comments(db: Session = Depends(get_db)):
    return (
        db.query(TenantComment)
        .order_by(TenantComment.created_at.desc())
        .all()
    )


# -----------------------------
# RESOLVE TENANT COMMENT
# -----------------------------
@router.post("/admin/comments/{comment_id}/resolve")
async def resolve_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    comment = (
        db.query(TenantComment)
        .filter(TenantComment.id == comment_id)
        .first()
    )

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.status = "resolved"
    comment.resolved_at = datetime.utcnow()
    db.commit()

    # Broadcast real-time update
    await manager.broadcast({
        "event": "comment_resolved",
        "comment_id": comment.id
    })

    return {"success": True}
