# app/services/notification_engine.py

import logging

from app.services.email_service import send_email
from app.services.whatsapp_service import send_whatsapp
from app.services.sms_service import send_sms
from app.services.pdf_service import generate_receipt_pdf


logger = logging.getLogger("notification_engine")


def notify_payment_success(payment, tenant):
    """
    Notify tenant when a payment is successful.
    """

    try:

        logger.info("Starting payment notification workflow")

        # Generate receipt PDF
        receipt_path = generate_receipt_pdf(payment)

        message = (
            f"Payment received successfully.\n"
            f"Amount: {payment.amount}\n"
            f"Reference: {payment.reference}"
        )

        # Send email
        if tenant.email:
            send_email(
                to=tenant.email,
                subject="Rent Payment Receipt",
                body=message,
                attachment=receipt_path,
            )

        # Send WhatsApp
        if tenant.phone:
            send_whatsapp(
                tenant.phone,
                f"Your payment was received. Ref: {payment.reference}"
            )

        # Send SMS
        if tenant.phone:
            send_sms(
                tenant.phone,
                f"Payment received. Ref: {payment.reference}"
            )

        logger.info("Payment notifications completed")

    except Exception as e:
        logger.exception("Payment notification failed: %s", e)


def notify_rent_due(tenant, amount, due_date):

    message = (
        f"Rent reminder.\n"
        f"Amount: {amount}\n"
        f"Due Date: {due_date}"
    )

    if tenant.email:
        send_email(
            to=tenant.email,
            subject="Rent Reminder",
            body=message,
        )

    if tenant.phone:
        send_whatsapp(
            tenant.phone,
            message
        )


def notify_penalty_applied(tenant, amount):

    message = f"A penalty of {amount} has been applied to your account."

    if tenant.email:
        send_email(
            to=tenant.email,
            subject="Penalty Notice",
            body=message,
        )

    if tenant.phone:
        send_sms(
            tenant.phone,
            message
        )
