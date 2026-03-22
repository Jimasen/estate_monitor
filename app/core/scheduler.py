# app/core/scheduler.py

import logging
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.services.rent_automation_service import (
    process_rent_reminders,
    process_late_payments,
)
from app.database.session import SessionLocal
from app.services.reminder_service import (
    run_rent_reminder_job,
    run_subscription_reminder_job,
)
from app.services.status_service import subscription_status
from app.websocket.status_socket import broadcast_to_tenant
from app.models.subscription import Subscription
from app.services.payment_service import auto_charge_subscription

logger = logging.getLogger("scheduler")

UTC = ZoneInfo("UTC")
scheduler = AsyncIOScheduler(timezone=UTC)


# --------------------------------------------------
# DAILY REMINDERS
# --------------------------------------------------
async def scheduled_reminders():
    logger.info("🔔 Starting DAILY reminder job (UTC)...")
    db = SessionLocal()
    try:
        await run_rent_reminder_job(db)
        await run_subscription_reminder_job(db)
        logger.info("✅ Daily reminders completed.")
    except Exception as e:
        logger.exception(f"❌ Reminder job failed: {e}")
    finally:
        db.close()


# --------------------------------------------------
# EXPIRY CHECK + SAFE BATCHING
# --------------------------------------------------
async def check_subscription_expiry():
    logger.info("🔎 Checking subscription expiry status...")
    db = SessionLocal()

    try:
        query = db.query(Subscription).yield_per(100)

        for sub in query:
            if not sub.user:
                continue

            user = sub.user
            status_data = subscription_status(user)

            try:
                await broadcast_to_tenant(
                    tenant_id=user.id,
                    message={
                        "type": "subscription_status_update",
                        "status": status_data.get("status"),
                        "plan": sub.plan,
                    },
                )
            except Exception as ws_error:
                logger.warning(f"⚠ WebSocket broadcast failed for user {user.id}: {ws_error}")

        logger.info("✅ Subscription expiry check completed.")

    except Exception as e:
        logger.exception(f"❌ Expiry check failed: {e}")
    finally:
        db.close()


# --------------------------------------------------
# AUTO CHARGE WRAPPER
# --------------------------------------------------
def auto_charge_with_logging(frequency: str):
    logger.info(f"💳 Starting {frequency.upper()} auto-charge...")
    db = SessionLocal()

    try:
        auto_charge_subscription(db=db, frequency=frequency)
        logger.info(f"✅ {frequency.upper()} auto-charge completed.")
    except Exception as e:
        logger.exception(f"❌ {frequency.upper()} auto-charge failed: {e}")
    finally:
        db.close()


# -------------------------------------------------
# SCHEDULED JOB
# -------------------------------------------------
def run_rent_automation():

    db = SessionLocal()

    try:

        process_rent_reminders(db)
        process_late_payments(db)

    finally:
        db.close()


# --------------------------------------------------
# START SCHEDULER
# --------------------------------------------------
def start_scheduler():
    if scheduler.running:
        logger.info("⚠ Scheduler already running.")
        return

    logger.info("🚀 Starting AsyncIO Scheduler (UTC)...")

    # Monthly Auto Charge
    scheduler.add_job(
        auto_charge_with_logging,
        trigger=CronTrigger(day=1, hour=0, minute=0, timezone=UTC),
        kwargs={"frequency": "monthly"},
        id="monthly_subscription",
        replace_existing=True,
        coalesce=True,
        misfire_grace_time=300,
    )

    # Yearly Auto Charge
    scheduler.add_job(
        auto_charge_with_logging,
        trigger=CronTrigger(month=1, day=1, hour=0, minute=0, timezone=UTC),
        kwargs={"frequency": "yearly"},
        id="yearly_subscription",
        replace_existing=True,
        coalesce=True,
        misfire_grace_time=300,
    )

    # Daily Reminders (8 AM UTC)
    scheduler.add_job(
        scheduled_reminders,
        trigger=CronTrigger(hour=8, minute=0, timezone=UTC),
        id="daily_reminders",
        replace_existing=True,
        coalesce=True,
        misfire_grace_time=300,
    )

    # Rent Automation
    scheduler.add_job(
    	run_rent_automation,
    	"cron",
    	hour=1
    )

    # Expiry Check Every Hour
    scheduler.add_job(
        check_subscription_expiry,
        trigger=IntervalTrigger(hours=1, timezone=UTC),
        id="subscription_expiry_check",
        replace_existing=True,
        coalesce=True,
        misfire_grace_time=300,
    )

    scheduler.start()
    logger.info("✅ Scheduler started successfully (UTC).")
