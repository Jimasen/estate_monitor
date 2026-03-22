# app/models/property_sale.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class PropertySale(Base):
    __tablename__ = "property_sales"

    id = Column(Integer, primary_key=True, index=True)
    property_name = Column(String(255), nullable=False)
    property_address = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

    # Fix table name: users, not user
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Explicitly tell SQLAlchemy which column is the foreign key
    seller = relationship("User", foreign_keys=[seller_id])
    buyer = relationship("User", foreign_keys=[buyer_id])
