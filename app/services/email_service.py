import yagmail
from app.core.config import settings


def send_email(
    to_email: str,
    tenant_name: str,
    pdf_bytes: bytes,
    filename: str
):
    yag = yagmail.SMTP(
        user=settings.EMAIL_USER,
        password=settings.EMAIL_PASSWORD
    )

    subject = "Rent Payment Receipt"

    body = f"""
Hello {tenant_name},

We acknowledge receipt of your rent payment.
Please find your official receipt attached.

Thank you for your cooperation.
God bless.

Estate Management
"""

    yag.send(
        to=to_email,
        subject=subject,
        contents=body,
        attachments=[(filename, pdf_bytes)]
    )
