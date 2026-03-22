
from sqlalchemy import Column, Integer, String, Text
from app.database.base import Base

class PageBlock(Base):
    __tablename__ = "page_blocks"

    id = Column(Integer, primary_key=True, index=True)
    section = Column(String(50))      # hero, feature, gallery, footer
    title = Column(String(255))
    subtitle = Column(Text)
    image_url = Column(String(500))
    button_text = Column(String(100))
    button_link = Column(String(200))
    position = Column(Integer)

