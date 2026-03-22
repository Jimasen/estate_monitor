# app/utils/notifications.py

from app.core.config import settings
import httpx
import logging

logger = logging.getLogger("notifications")


async def send_whatsapp(to: str, message: str):
    """Send a WhatsApp message asynchronously."""
    if not settings.WHATSAPP_ENABLED:
        return

    url = f"https://graph.facebook.com/v17.0/{settings.WHATSAPP_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"}
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message},
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(url, headers=headers, json=data)
        logger.info(f"WhatsApp sent to {to}")
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message to {to}: {e}")


async def send_sms(to: str, message: str):
    """Send SMS asynchronously."""
    if not settings.SMS_ENABLED:
        return

    # Replace with async SMS API if available; for now just log
    logger.info(f"SMS to {to}: {message}")


async def notify_user(to: str, message: str, via: str = "whatsapp"):
    """Unified async notification."""
    if via.lower() == "whatsapp":
        await send_whatsapp(to, message)
    elif via.lower() == "sms":
        await send_sms(to, message)
    else:
        logger.warning(f"Unknown notification type: {via}")
