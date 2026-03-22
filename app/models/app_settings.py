# app/models/app_settings.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.base import Base

class AppSettings(Base):
    __tablename__ = "app_settings"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    app_name = Column(String(150), default="Property & Business Management Platform")
    logo_url = Column(String(255))
    primary_color = Column(String(50), default="#0d6efd")
    whatsapp_number = Column(String(50))
    facebook_page = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
