from app.database.session import SessionLocal
from app.models.email_queue import EmailQueue


def queue_email(to_email, tenant_name, pdf_bytes, filename, error):
    db = SessionLocal()
    email = EmailQueue(
        to_email=to_email,
        tenant_name=tenant_name,
        pdf=pdf_bytes,
        filename=filename,
        last_error=error
    )
    db.add(email)
    db.commit()
    db.close()
