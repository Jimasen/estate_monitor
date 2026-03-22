from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    estate_id = Column(Integer, ForeignKey("estates.id"), nullable=False)

    estate = relationship("Estate", back_populates="properties")
    tenants = relationship("Tenant", back_populates="property")
