# app/services/payments/flutterwave_service.py
import os
import requests

def create_payment(amount: float, email: str, reference: str, redirect_url: str):
    secret = os.getenv("FLUTTERWAVE_SECRET_KEY")
    if not secret:
        raise Exception("Flutterwave not configured")

    payload = {
        "tx_ref": reference,
        "amount": amount,
        "currency": "NGN",
        "redirect_url": redirect_url,
        "customer": {
            "email": email
        }
    }

    headers = {
        "Authorization": f"Bearer {secret}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.flutterwave.com/v3/payments",
        json=payload,
        headers=headers,
        timeout=30,
    )

    return response.json()

# Verify a Flutterwave transaction
def verify_payment(reference: str):
    secret = os.getenv("FLUTTERWAVE_SECRET_KEY")
    if not secret:
        raise Exception("Flutterwave not configured")

    headers = {
        "Authorization": f"Bearer {secret}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        f"https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={reference}",
        headers=headers,
        timeout=30,
    )

    return response.json()
