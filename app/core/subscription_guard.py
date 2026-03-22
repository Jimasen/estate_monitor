# app/core/subscription_guard.py

from fastapi import Depends, HTTPException, status
from app.api.auth.dependencies import get_current_user
from app.services.status_service import subscription_status


# --------------------------------------------------
# CORE ENFORCEMENT LOGIC
# --------------------------------------------------

def _validate_subscription(user):
    data = subscription_status(user)

    # Overdue / Expired
    if data["status"] in ["overdue", "expired"]:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Subscription expired or overdue. Please renew."
        )

    # Not active at all
    if data["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Active subscription required."
        )

    return data


# --------------------------------------------------
# DEPENDENCY: REQUIRE ACTIVE SUBSCRIPTION
# --------------------------------------------------

def enforce_active_subscription(
    current_user = Depends(get_current_user)
):
    _validate_subscription(current_user)
    return current_user


# --------------------------------------------------
# DEPENDENCY: REQUIRE SPECIFIC PLAN
# --------------------------------------------------

def require_plan(*allowed_plans: str):
    def dependency(current_user = Depends(get_current_user)):
        data = _validate_subscription(current_user)

        if data.get("plan") not in allowed_plans:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Upgrade your subscription plan to access this feature."
            )

        return current_user

    return dependency


# --------------------------------------------------
# DIRECT USAGE (For Services / Internal Calls)
# --------------------------------------------------

def enforce_subscription(user):
    return _validate_subscription(user)
