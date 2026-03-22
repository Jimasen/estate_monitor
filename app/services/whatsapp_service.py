# app/services/whatsapp_service.py
import requests
from app.core.config import settings

def _get_api_url() -> str:
    if not settings.WHATSAPP_PHONE_ID:
        raise RuntimeError("WhatsApp is enabled but WHATSAPP_PHONE_ID is missing")
    return f"https://graph.facebook.com/v19.0/{settings.WHATSAPP_PHONE_ID}/messages"

def send_whatsapp_text(phone: str, message: str):
    """Send a text WhatsApp message"""
    if not settings.WHATSAPP_ENABLED:
        return {"status": "skipped", "response": None, "error": "WhatsApp disabled"}

    if not settings.WHATSAPP_PHONE_ID or not settings.WHATSAPP_ACCESS_TOKEN:
        raise RuntimeError("WhatsApp enabled but not fully configured")

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message},
    }
    return _send(payload, phone)

def send_whatsapp_document(phone: str, doc_url: str, filename: str, caption: str = None):
    """Send a document (PDF, etc.) via WhatsApp"""
    if not settings.WHATSAPP_ENABLED:
        return {"status": "skipped", "response": None, "error": "WhatsApp disabled"}

    if not settings.WHATSAPP_PHONE_ID or not settings.WHATSAPP_ACCESS_TOKEN:
        raise RuntimeError("WhatsApp enabled but not fully configured")

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "document",
        "document": {
            "link": doc_url,
            "filename": filename,
        },
    }

    if caption:
        payload["document"]["caption"] = caption

    return _send(payload, phone)

def _send(payload: dict, phone: str):
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            _get_api_url(),
            headers=headers,
            json=payload,
            timeout=10,
        )

        if not response.ok:
            print("[WHATSAPP ERROR RESPONSE]", response.text)

        response.raise_for_status()
        print(f"[WHATSAPP SENT] {phone}")

        return {"status": "sent", "response": response.json(), "error": None}

    except requests.exceptions.RequestException as e:
        print(f"[WHATSAPP ERROR] {phone} | {str(e)}")
        return {"status": "failed", "response": None, "error": str(e)}
