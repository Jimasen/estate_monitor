from app.core.celery_app import celery

@celery.task
def send_background_email(email: str):
    print(f"Sending email to {email}")
