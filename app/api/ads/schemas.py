# app/api/ads/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class PropertyAdCreate(BaseModel):
    title: str
    price: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = []
    contact_phone: Optional[str] = None
    whatsapp_link: Optional[str] = None
    facebook_link: Optional[str] = None
    is_featured: Optional[bool] = False
