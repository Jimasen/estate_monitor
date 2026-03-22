from fastapi import Depends, HTTPException, status
from app.core.session import get_current_user

def require_role(*allowed_roles):
    def guard(user = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return user
    return guard
