from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True)

    wallet_id = Column(Integer, ForeignKey("wallets.id"))

    amount = Column(Float)

    transaction_type = Column(String(50), nullable=False)
    # credit / debit

    reference = Column(String(255), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
