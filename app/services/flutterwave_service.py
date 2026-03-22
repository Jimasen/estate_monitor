# app/services/paystack_service.py
import requests, os

PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET_KEY")

def create_payment(amount, email, reference, callback_url):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET}"}
    payload = {
        "email": email,
        "amount": int(amount * 100),  # Paystack expects kobo
        "reference": reference,
        "callback_url": callback_url
    }
    res = requests.post(url, headers=headers, json=payload)
    res.raise_for_status()
    return res.json()["data"]["authorization_url"]

def verify_payment(reference: str) -> bool:
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    data = res.json().get("data", {})
    return data.get("status") == "success"
