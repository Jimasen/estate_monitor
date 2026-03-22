# app/schemas/property.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ----- Schema for creating a new ad -----
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
    is_approved: Optional[bool] = False

    model_config = {"from_attributes": True}

# ----- Schema for returning an ad (response) -----
class PropertyAdSchema(BaseModel):
    id: int
    title: str
    price: Optional[str]
    location: Optional[str]
    description: Optional[str]
    images: Optional[List[str]]
    contact_phone: Optional[str]
    whatsapp_link: Optional[str]
    facebook_link: Optional[str]
    is_featured: bool
    is_approved: bool
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}

# ----- Schema for returning UserMedia -----
class UserMediaSchema(BaseModel):
    id: int
    filename: str
    url: str
    uploaded_by: Optional[int]  # user id
    created_at: Optional[datetime]
    is_approved: Optional[bool] = False

    model_config = {"from_attributes": True}
