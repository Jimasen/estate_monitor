# app/api/tenant/schemas.py
from pydantic import BaseModel, Field, validator
import re

class TenantCreateRequest(BaseModel):
    full_name: str
    phone: str = Field(..., example="+234739630505")
    property_id: int

    @validator("phone")
    def validate_phone(cls, v):
        pattern = r"^\+\d{6,15}$"  # + followed by 6-15 digits
        if not re.match(pattern, v):
            raise ValueError("Phone number must be in international format starting with '+' and country code")
        return v
