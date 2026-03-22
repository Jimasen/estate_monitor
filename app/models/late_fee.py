# app/models/late_fee.py
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base
from app.models.payment import RentPayment  # import the existing RentPayment

class LateFee(Base):
    __tablename__ = "late_fees"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("rent_payments.id"), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationship to RentPayment
    payment = relationship("RentPayment", back_populates="late_fees")
