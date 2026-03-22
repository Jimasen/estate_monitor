# app/models/activity_log.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class ActivityLog(Base):

    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    event_type = Column(String(100), nullable=False)

    description = Column(String(255), nullable=False)

    extra_data = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
