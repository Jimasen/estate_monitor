# app/api/billing/routes.py

import os
import requests
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.subscription import Subscription
from app.models.pricing_plan import PricingPlan
from app.core.dependencies import get_current_user
from app.services.status_service import subscription_status
from app.websocket.status_socket import broadcast_to_tenant

router = APIRouter(
    prefix="/billing",
    tags=["Billing"]
)

PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET")


# ==============================
# 1️⃣ INITIALIZE PAYMENT
# ==============================
@router.get("/initialize/{plan_name}")
def initialize_payment(
    plan_name: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    plan = db.query(PricingPlan).filter(
        PricingPlan.name == plan_name
    ).first()

    if not plan:
        raise HTTPException(404, "Plan not found")

    payload = {
        "email": current_user.email,
        "amount": int(plan.price * 100),  # Paystack uses kobo
        "callback_url": f"https://yourdomain.com/billing/verify/{plan.name}",
        "metadata": {
            "tenant_id": current_user.tenant_id,
            "user_id": current_user.id,
            "plan": plan.name
        }
    }

    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        json=payload,
        headers={"Authorization": f"Bearer {PAYSTACK_SECRET}"}
    ).json()

    if not response.get("status"):
        raise HTTPException(400, "Failed to initialize payment")

    return response["data"]


# ==============================
# 2️⃣ VERIFY PAYMENT & ACTIVATE
# ==============================
@router.get("/verify/{plan_name}")
async def verify_payment(
    plan_name: str,
    reference: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Verify transaction with Paystack
    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers={"Authorization": f"Bearer {PAYSTACK_SECRET}"}
    ).json()

    if not response.get("status"):
        raise HTTPException(400, "Payment verification failed")

    data = response.get("data")

    if data.get("status") != "success":
        raise HTTPException(400, "Payment not successful")

    # Get selected plan
    plan = db.query(PricingPlan).filter(
        PricingPlan.name == plan_name
    ).first()

    if not plan:
        raise HTTPException(404, "Plan not found")

    # Get or create subscription
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()

    if not subscription:
        subscription = Subscription(user_id=current_user.id)
        db.add(subscription)

    # Activate subscription
    subscription.activate(
        days=plan.duration_days,
        plan=plan.name
    )

    db.commit()
    db.refresh(subscription)

    # Get updated subscription status
    status_data = subscription_status(current_user)

    # 🔥 REAL-TIME TENANT BROADCAST
    await broadcast_to_tenant(
        tenant_id=current_user.tenant_id,
        message={
            "type": "subscription_status_update",
            "status": status_data["status"],
            "plan": plan.name,
            "expires_at": subscription.expires_at.isoformat(),
        }
    )

    return {
        "message": "Subscription activated successfully",
        "plan": plan.name,
        "expires_at": subscription.expires_at
    }


# ==============================
# 3️⃣ GET CURRENT SUBSCRIPTION
# ==============================
@router.get("/status")
def get_subscription_status(
    current_user=Depends(get_current_user),
):
    return subscription_status(current_user)
