# app/api/admin/scheduler_routes.py
from fastapi import APIRouter
from app.core.scheduler_triggers import (
    trigger_daily_reminders,
    trigger_monthly_charge,
    trigger_yearly_charge,
)

router = APIRouter(
    prefix="/admin/scheduler",
    tags=["Admin Scheduler"],
)


@router.post("/run-daily-reminders")
async def run_daily_reminders():
    await trigger_daily_reminders()
    return {"message": "Daily reminders executed successfully (UTC)."}


@router.post("/run-monthly-charge")
async def run_monthly_charge():
    await trigger_monthly_charge()
    return {"message": "Monthly auto-charge executed successfully (UTC)."}


@router.post("/run-yearly-charge")
async def run_yearly_charge():
    await trigger_yearly_charge()
    return {"message": "Yearly auto-charge executed successfully (UTC)."}
