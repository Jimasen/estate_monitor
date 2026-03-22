# app/models/role.py
from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
