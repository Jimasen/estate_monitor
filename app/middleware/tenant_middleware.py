from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.tenant_resolver import get_tenant_db


class TenantMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        domain = request.headers.get("X-Company-Domain")
        tenant_id = request.headers.get("X-Tenant-Id")  # ADD THIS

        if domain:
            request.state.tenant_db = get_tenant_db(domain)

        # attach tenant_id globally
        if tenant_id:
            request.state.tenant_id = int(tenant_id)
        else:
            request.state.tenant_id = None

        response = await call_next(request)

        return response
