from app.database.session import SessionLocal
from app.models.audit_log import AuditLog

def log_action(user_id: int, action: str, ip: str):
    db = SessionLocal()
    db.add(AuditLog(
        user_id=user_id,
        action=action,
        ip_address=ip
    ))
    db.commit()
