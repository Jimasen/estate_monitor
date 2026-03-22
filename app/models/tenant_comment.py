from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, func, Index
from sqlalchemy.orm import relationship
from app.database.base import Base

class TenantComment(Base):
    __tablename__ = "tenant_comments"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    comment = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_internal = Column(Boolean, default=True)
    visibility = Column(String(20), default="private")
    is_deleted = Column(Boolean, default=False)
