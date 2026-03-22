# app/services/cron_jobs.py

from apscheduler.schedulers.background import BackgroundScheduler
from app.services.payout_scheduler import process_landlord_payouts
from app.services.risk_scanner import scan_all_tenants
from app.services.payment_service import auto_charge_subscription
from app.database.session import SessionLocal
import logging

scheduler = BackgroundScheduler()

# -----------------------
# Payouts Job
# -----------------------
def payout_job():
    db = SessionLocal()
    try:
        logging.info("Running landlord payout job...")
        process_landlord_payouts(db)
    except Exception as e:
        logging.error(f"Payout job failed: {e}")
    finally:
        db.close()

# -----------------------
# Risk Scan Job
# -----------------------
def risk_scan_job():
    db = SessionLocal()
    try:
        logging.info("Running risk scan job...")
        scan_all_tenants(db)
    except Exception as e:
        logging.error(f"Risk scan job failed: {e}")
    finally:
        db.close()

# -----------------------
# Subscription Auto-Charge Job
# -----------------------
def subscription_job(frequency: str):
    db = SessionLocal()
    try:
        logging.info(f"Running subscription auto-charge ({frequency})...")
        auto_charge_subscription(db, frequency)
    except Exception as e:
        logging.error(f"Subscription job failed: {e}")
    finally:
        db.close()

# -----------------------
# Scheduler Starter
# -----------------------
def start_scheduler():
    # Daily landlord payouts at midnight UTC
    scheduler.add_job(payout_job, trigger="cron", hour=0, minute=0, id="payout_job", replace_existing=True)

    # Risk scans daily at 2am UTC
    scheduler.add_job(risk_scan_job, trigger="cron", hour=2, minute=0, id="risk_scan_job", replace_existing=True)

    # Subscription auto-charge
    scheduler.add_job(lambda: subscription_job("monthly"), trigger="cron", hour=3, minute=0, id="monthly_subs", replace_existing=True)
    scheduler.add_job(lambda: subscription_job("annual"), trigger="cron", hour=4, minute=0, id="annual_subs", replace_existing=True)

    scheduler.start()
    logging.info("Unified scheduler started with payouts, risk scans, and subscription charges.")
