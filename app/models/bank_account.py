from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    account_name = Column(String(150), nullable=False)

    account_number = Column(String(50), nullable=False)

    bank_code = Column(String(20), nullable=False)

    provider = Column(String, default="paystack")
