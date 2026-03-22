from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime, Boolean, func
from app.database.base import Base


class UserComment(Base):
    __tablename__ = "user_comments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    comment = Column(Text, nullable=False)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    visibility = Column(String(20), default="private")
    is_internal = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
