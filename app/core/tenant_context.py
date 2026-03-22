# app/core/tenant_context.py

from fastapi import Depends, HTTPException
from app.models.user import User

def get_tenant_id(current_user: User) -> int:
    """
    SaaS tenant resolver.
    For now:
    - One tenant = one user account (owner-based SaaS)
    - Later: can be upgraded to organizations/companies
    """
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Unauthenticated")

    return current_user.id
