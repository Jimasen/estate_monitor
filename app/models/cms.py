from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from app.database.base import Base

class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String, unique=True)


class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey("pages.id"))
    type = Column(String)
    position = Column(Integer)  # ORDER CONTROL
    config = Column(JSON)       # size, columns, etc


class BlockItem(Base):
    __tablename__ = "block_items"

    id = Column(Integer, primary_key=True)
    block_id = Column(Integer, ForeignKey("blocks.id"))
    content = Column(JSON)  # title, image, link, etc
