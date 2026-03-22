from datetime import date
from sqlalchemy.orm import Session

from app.services.payment_status_service import get_payment_status_indicator
from app.models.payment import RentPayment
from app.models.user import User
from app.services.penalty_service import apply_late_fee

from app.services.email_service import send_email
from app.services.sms_service import send_sms
from app.services.whatsapp_service import (
    send_whatsapp_text,
    send_whatsapp_document,
)

from app.services.status_service import rent_status, subscription_status
from app.services.tenant_service import auto_suspend_tenant
from app.services.invoice_service import generate_invoice
from app.websocket.status_socket import broadcast

from app.core.config import settings


# ----------------------------
# RENT REMINDERS
# ----------------------------
async def run_rent_reminder_job(db: Session):
    today = date.today()
    payments = db.query(RentPayment).filter(RentPayment.status == "pending").all()

    for payment in payments:
        if not payment.due_date:
            continue

        status = get_payment_status_indicator(payment)
        tenant = payment.tenant

        # 🔥 Real-time WebSocket broadcast (tenant-based)
        await broadcast(payment.tenant.property.estate.tenant_id if hasattr(payment.tenant.property.estate, "tenant_id") else 0, {
            "type": "rent_status_update",
            "tenant_id": tenant.id,
            "status": status
        })

        days_left = (payment.due_date - today).days

        # ----------------------------
        # READY REMINDERS (7, 3, 1 days before due)
        # ----------------------------
        if status == "ready" and days_left in (7, 3, 1):
            send_rent_reminder(payment, days_left, status)

        # ----------------------------
        # OVERDUE LOGIC
        # ----------------------------
        elif status == "overdue":

            # ✅ Apply late fee properly
            apply_late_fee(payment, db)

            # 1️⃣ Suspend tenant
            auto_suspend_tenant(payment, db)

            # 2️⃣ Generate invoice
            pdf_path = generate_invoice(payment)
            doc_url = f"{settings.PUBLIC_BASE_URL}/{pdf_path}"

            # 3️⃣ Send invoice via WhatsApp
            if tenant.phone and getattr(settings, "WHATSAPP_ENABLED", False):
                send_whatsapp_document(
                    phone=tenant.phone,
                    doc_url=doc_url,
                    filename="Rent_Invoice.pdf",
                    caption="❌ Your overdue rent invoice. Please pay immediately."
                )

            # 4️⃣ Send reminders
            send_rent_reminder(payment, days_left, status)


def send_rent_reminder(payment: RentPayment, days_left: int, status: str):
    tenant = payment.tenant
    owner = tenant.property.estate.owner

    amount_value = float(payment.amount_due)
    amount_display = f"₦{amount_value:,.2f}"
    due_date = payment.due_date.strftime("%Y-%m-%d")

    alert_icon = "❌" if status == "overdue" else "⚠"
    urgency = "OVERDUE" if status == "overdue" else "Due Soon"

    tenant_message = (
        f"{alert_icon} Hello {tenant.full_name},\n\n"
        f"Your rent of {amount_display} "
        f"is due on {due_date}.\n"
        f"Days left: {days_left}.\n"
        f"Status: {urgency}.\n\n"
        f"— Estate Monitor"
    )

    # SMS
    if tenant.phone and getattr(settings, "SMS_ENABLED", True):
        send_sms(tenant.phone, tenant_message)

    # WhatsApp text
    if tenant.phone and getattr(settings, "WHATSAPP_ENABLED", False):
        send_whatsapp_text(tenant.phone, tenant_message)

    # Owner email
    if owner and owner.email:
        subject = f"Rent Alert - {urgency}"
        email_message = f"""
Tenant: {tenant.full_name}
Unit: {tenant.property.unit_name}
Amount Due: {amount_display}
Due Date: {due_date}
Days Left: {days_left}
Status: {status.upper()}
"""
        send_email(owner.email, subject, email_message.strip())


# ----------------------------
# SUBSCRIPTION REMINDERS
# ----------------------------
async def run_subscription_reminder_job(db: Session):
    users = db.query(User).all()

    for user in users:
        status_data = subscription_status(user)
        status = status_data["status"]

        # Broadcast subscription status
        await broadcast(0, {
            "type": "subscription_status_update",
            "user_id": user.id,
            "status": status
        })

        if status in ("ready", "overdue"):
            send_subscription_reminder(user, status)


def send_subscription_reminder(user: User, status: str):
    icon = "❌" if status == "overdue" else "⚠"
    message_type = (
        "Subscription Overdue"
        if status == "overdue"
        else "Subscription Expiring Soon"
    )

    message = (
        f"{icon} Hello {user.full_name},\n\n"
        f"{message_type}.\n"
        f"Please renew to avoid service interruption.\n\n"
        f"— Estate Monitor"
    )

    if user.phone and getattr(settings, "WHATSAPP_ENABLED", False):
        send_whatsapp_text(user.phone, message)
