# app/services/sms_service.py

import requests
from app.core.config import settings
from typing import Dict

AFRICAS_TALKING_URL = "https://api.africastalking.com/version1/messaging"


def send_sms(phone: str, message: str) -> Dict:
    headers = {
        "apiKey": settings.SMS_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    data = {
        "username": settings.SMS_USERNAME,  # sandbox or production
        "to": phone,
        "message": message,
        "from": settings.SMS_SENDER,
    }

    try:
        response = requests.post(
            AFRICAS_TALKING_URL,
            headers=headers,
            data=data,
            timeout=10,
        )
        response.raise_for_status()

        return {
            "status": "sent",
            "provider": "africastalking",
            "data": response.json(),
        }

    except requests.exceptions.Timeout:
        return {
            "status": "failed",
            "error": "SMS request timed out",
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": "failed",
            "error": str(e),
        }
