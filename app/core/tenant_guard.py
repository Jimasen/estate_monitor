# app/core/tenant_guard.py

from fastapi import Depends, HTTPException
from app.core.session import get_current_user


# --------------------------------------------------
# TENANT ISOLATION GUARD
# Prevents cross-tenant data access
# --------------------------------------------------
def tenant_scope(resource_tenant_id: int):
    def guard(user = Depends(get_current_user)):
        if user.tenant_id != resource_tenant_id:
            raise HTTPException(
                status_code=403,
                detail="Tenant isolation violation"
            )
        return user
    return guard


# --------------------------------------------------
# BLOCK SUSPENDED TENANT
# Prevent suspended tenants from accessing system
# --------------------------------------------------
def enforce_active_tenant(tenant):
    if not tenant.is_active:
        raise HTTPException(
            status_code=403,
            detail="Tenant suspended due to overdue subscription or rent."
        )
