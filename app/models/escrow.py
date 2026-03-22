
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class Escrow(Base):
    __tablename__ = "escrows"

    id = Column(Integer, primary_key=True)

    tenant_id = Column(Integer, ForeignKey("users.id"))
    landlord_id = Column(Integer, ForeignKey("users.id"))

    payment_id = Column(Integer)

    amount = Column(Float)

    status = Column(String, default="held")
    # held / released / refunded

    created_at = Column(DateTime, server_default=func.now())
