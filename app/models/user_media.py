from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class UserMedia(Base):
    __tablename__ = "user_media"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    media_type = Column(String(50))  # image, video, banner
    file_path = Column(String(255), nullable=False)

    # ⚠ Needs replacement since User is gone
    user_id = Column(Integer, ForeignKey("users.id"))

    # user = relationship("User", back_populates="media")
