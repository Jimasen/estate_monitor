# app/models/tenant.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)

    # contact
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), unique=True, nullable=False)

    # relations
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)

    # rent tracking
    rent_due_date = Column(Date, nullable=True)

    # AI Risk Score
    risk_score = Column(Float, default=0)

    # timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # relationships
    property = relationship("Property", back_populates="tenants")
    company = relationship("Company", back_populates="tenants")

    rent_payments = relationship(
        "RentPayment",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )
