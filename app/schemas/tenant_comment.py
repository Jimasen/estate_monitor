from pydantic import BaseModel
from datetime import datetime

class TenantCommentBase(BaseModel):
    tenant_id: int
    comment: str

class TenantCommentCreate(TenantCommentBase):
    pass

class TenantCommentOut(TenantCommentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
