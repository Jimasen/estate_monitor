from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User


def get_admin_metrics(db: Session):
    """
    Global admin metrics
    """
    total_users = db.query(User).count()

    return {
        "total_users": total_users,
    }


def get_owner_dashboard(db: Session, owner_id: int):
    """
    Owner-specific metrics
    """
    user_count = db.query(User).filter(User.id == owner_id).count()

    return {
        "user_count": user_count,
    }
