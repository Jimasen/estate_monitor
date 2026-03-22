# app/models/audit_log.py
from sqlalchemy import Column, Integer, String, DateTime
from app.database.base import Base
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    action = Column(String(255))
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)
