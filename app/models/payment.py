# app/models/payment.py

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database.base import Base


class RentPayment(Base):
    __tablename__ = "rent_payments"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)

    amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending", nullable=False)

    due_date = Column(DateTime, nullable=False)

    paid_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    gateway = Column(String(50), nullable=False, default="")
    reference = Column(String(100), unique=True, nullable=False)

    tenant = relationship("Tenant", back_populates="rent_payments")

    late_fees = relationship(
        "LateFee",
        back_populates="payment",
        cascade="all, delete-orphan"
    )


# BACKWARD COMPATIBILITY
Payment = RentPayment
