# app/core/saas_guard.py

from fastapi import HTTPException

def require_active_subscription(user):
    """
    SaaS access guard.
    Free for now — paid later.
    """
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Future:
    # if not user.subscription or user.subscription.expired():
    #     raise HTTPException(status_code=402, detail="Subscription required")

    return True
