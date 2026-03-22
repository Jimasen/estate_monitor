from sqlalchemy import Column, Integer, String
from app.database.base import Base

class CorporateAccount(Base):
    __tablename__ = "corporate_accounts"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    contact_email = Column(String(150))
