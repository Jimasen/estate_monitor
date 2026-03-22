# app/models/estate.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Estate(Base):
    __tablename__ = "estates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("owners.id"))

    # Relationships
    owner = relationship("Owner", back_populates="estates")
    properties = relationship("Property", back_populates="estate")
    utility_bills = relationship("UtilityBill", back_populates="estate", cascade="all, delete-orphan")
