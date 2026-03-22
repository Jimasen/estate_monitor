# app/core/event_handlers.py

import logging
import asyncio
from app.core.events import on, TENANT_CREATED, RENT_DUE, PAYMENT_RECEIVED
from app.utils.notifications import notify_user
from app.services.realtime_event_service import broadcast_event
from app.services.risk_scoring_service import calculate_tenant_risk
from app.database.async_session import async_db_session  # async-safe DB context

logger = logging.getLogger("event_handlers")


# -------------------------------
# RENT LATE
# -------------------------------
@on("rent_late")
async def handle_rent_late(data: dict):
    tenant = data.get("tenant")
    if not tenant:
        return

    try:
        await notify_user(
            tenant.phone,
            f"Your rent payment is overdue for {tenant.property_name}. Please make payment."
        )
    except Exception as e:
        logger.error(f"[rent_late] Failed to notify tenant {tenant.id}: {e}")


# -------------------------------
# RENT CRITICAL
# -------------------------------
@on("rent_critical")
async def handle_rent_critical(data: dict):
    tenant = data.get("tenant")
    if not tenant:
        return

    try:
        await notify_user(
            tenant.phone,
            "URGENT: Your rent is more than 7 days overdue. Immediate action required."
        )
    except Exception as e:
        logger.error(f"[rent_critical] Failed to notify tenant {tenant.id}: {e}")


# -------------------------------
# TENANT CREATED
# -------------------------------
@on(TENANT_CREATED)
async def handle_new_tenant(data: dict):
    tenant = data.get("tenant")
    if not tenant:
        return

    try:
        await notify_user(
            tenant.phone,
            f"Welcome {tenant.name}. You have been added to Estate Monitor."
        )
    except Exception as e:
        logger.error(f"[tenant_created] Failed to notify tenant {tenant.id}: {e}")

    try:
        # Optional DB audit/log
        async with async_db_session() as db:
            pass
    except Exception as e:
        logger.error(f"[tenant_created] DB session error: {e}")

    try:
        await broadcast_event(
            "tenant_created",
            {
                "tenant_id": tenant.id,
                "name": tenant.name,
                "property": tenant.property_name
            }
        )
    except Exception as e:
        logger.error(f"[tenant_created] Failed to broadcast event: {e}")


# -------------------------------
# RENT DUE
# -------------------------------
@on(RENT_DUE)
async def handle_rent_due(data: dict):
    tenant = data.get("tenant")
    if not tenant:
        return

    logger.info(f"Handling rent_due for tenant {tenant.id}")

    try:
        await notify_user(
            tenant.phone,
            f"Reminder: Rent for {tenant.property_name} is due."
        )
    except Exception as e:
        logger.error(f"[rent_due] Failed to notify tenant {tenant.id}: {e}")


# -------------------------------
# PAYMENT RECEIVED
# -------------------------------
@on(PAYMENT_RECEIVED)
async def handle_payment(data: dict):
    tenant = data.get("tenant")
    if not tenant:
        return

    try:
        async with async_db_session() as db:
            # Run sync-heavy risk scoring in background thread
            await asyncio.to_thread(calculate_tenant_risk, db, tenant.id)
    except Exception as e:
        logger.error(f"[payment_received] DB/risk scoring failed for tenant {tenant.id}: {e}")

    try:
        await notify_user(
            tenant.phone,
            "Payment received successfully. Thank you."
        )
    except Exception as e:
        logger.error(f"[payment_received] Failed to notify tenant {tenant.id}: {e}")

    try:
        await broadcast_event(
            "payment_received",
            {
                "tenant_id": tenant.id,
                "amount": data.get("amount")
            }
        )
    except Exception as e:
        logger.error(f"[payment_received] Failed to broadcast event for tenant {tenant.id}: {e}")
