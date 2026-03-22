from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class OwnerProfile(Base):
    __tablename__ = "owner_profiles"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    # Replace user_id with owner_id since User is gone
    owner_id = Column(Integer, ForeignKey("owners.id", ondelete="CASCADE"), unique=True, nullable=False)

    address = Column(String(255), nullable=True)
    company = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    owner = relationship("Owner", back_populates="profile")

    def __repr__(self):
        return f"<OwnerProfile owner_id={self.owner_id}>"
