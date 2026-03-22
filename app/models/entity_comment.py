from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class EntityComment(Base):
    __tablename__ = "entity_comments"

    id = Column(Integer, primary_key=True, index=True)
    estate_id = Column(Integer, ForeignKey("estates.id"), nullable=False, index=True)
    entity_type = Column(String(150), nullable=False, index=True)
    entity_id = Column(String(150), nullable=False, index=True)
    comment = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    parent_id = Column(Integer, ForeignKey("entity_comments.id"), nullable=True, index=True)
    is_internal = Column(Boolean, default=True)
    visibility = Column(String(20), default="private")
    is_deleted = Column(Boolean, default=False)

    replies = relationship("EntityComment", backref="parent", remote_side=[id])

    __table_args__ = (
        Index("ix_entity_comment_lookup", "estate_id", "entity_type", "entity_id"),
    )
