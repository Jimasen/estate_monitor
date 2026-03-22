from pydantic import BaseModel
from typing import List, Optional

class OwnerBase(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None

class OwnerCreate(OwnerBase):
    pass

class OwnerOut(OwnerBase):
    id: int

    class Config:
        orm_mode = True
