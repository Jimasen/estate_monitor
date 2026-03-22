from apscheduler.schedulers.background import BackgroundScheduler
from app.workers.tasks import rent_reminder_job


scheduler = BackgroundScheduler()

scheduler.add_job(
    rent_reminder_job,
    "interval",
    hours=24
)

scheduler.start()
