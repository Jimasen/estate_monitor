# app/models/marketing.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base

class RecommendationBlock(Base):
    __tablename__ = "recommendation_blocks"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    image_url = Column(String(500))
    link_url = Column(String(500))
    position = Column(String(50), default="homepage")
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())

class CarouselAd(Base):
    __tablename__ = "carousel_ads"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    image_url = Column(String(500), nullable=False)
    headline = Column(String(255))
    sub_text = Column(String(255))
    link_url = Column(String(500))
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
