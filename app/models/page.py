from sqlalchemy import Column, Integer, String, Text, Boolean
from app.database.base import Base


class Page(Base):

    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    slug = Column(String, unique=True, index=True)

    content = Column(Text)

    is_published = Column(Boolean, default=True)

