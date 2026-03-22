# app/models/investment.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    investor_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # <- use 'users'
    amount = Column(Float, nullable=False)
    status = Column(String(50), default="active")  # e.g., active, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    investor = relationship("User", foreign_keys=[investor_id])
