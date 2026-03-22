# app/core/scheduler_triggers.py
import asyncio
import logging
from app.database.session import SessionLocal
from app.services.reminder_service import run_rent_reminder_job, run_subscription_reminder_job
from app.services.payment_service import auto_charge_subscription 

logger = logging.getLogger("scheduler")

# ------------------------------
# DAILY REMINDERS
# ------------------------------
async def trigger_daily_reminders():
    logger.info("Running DAILY reminders manually (UTC)...")
    db = SessionLocal()
    try:
        await run_rent_reminder_job(db)
        await run_subscription_reminder_job(db)
        logger.info("Daily reminders executed.")
    except Exception as e:
        logger.exception(f"Daily reminder manual trigger failed: {e}")
    finally:
        db.close()

# ------------------------------
# MONTHLY CHARGE
# ------------------------------
async def trigger_monthly_charge():
    logger.info("Running MONTHLY auto-charge manually (UTC)...")
    try:
        await asyncio.to_thread(auto_charge_subscription, frequency="monthly")
        logger.info("Monthly auto-charge executed.")
    except Exception as e:
        logger.exception(f"Monthly charge manual trigger failed: {e}")

# ------------------------------
# YEARLY CHARGE
# ------------------------------
async def trigger_yearly_charge():
    logger.info("Running YEARLY auto-charge manually (UTC)...") 
    try:
        await asyncio.to_thread(auto_charge_subscription, frequency="yearly")
        logger.info("Yearly auto-charge executed.")
    except Exception as e:
        logger.exception(f"Yearly charge manual trigger failed: {e}")
