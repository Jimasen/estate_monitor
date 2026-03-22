# app/schemas/tenant.py

from pydantic import BaseModel, Field, validator
import re

class TenantCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: str = Field(..., example="+2348012345678")
    property_id: int | None = None  # optional property assignment

    @validator("phone")
    def validate_phone(cls, v):
        # Ensure phone starts with + and country code followed by digits
        if not re.fullmatch(r"\+\d{7,15}", v):
            raise ValueError("Phone number must start with +countrycode and contain 7-15 digits")
        return v
