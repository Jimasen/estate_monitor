# app/services/payments/paystack_service.py

import os
import requests


PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET_KEY")


# --------------------------------------
# Create Payment
# --------------------------------------
def create_payment(amount: float, email: str, reference: str, redirect_url: str):

    url = "https://api.paystack.co/transaction/initialize"

    payload = {
        "email": email,
        "amount": int(amount * 100),  # Paystack uses kobo
        "reference": reference,
        "callback_url": redirect_url
    }

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()


# --------------------------------------
# Verify Payment
# --------------------------------------
def verify_payment(reference: str):

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET}"
    }

    response = requests.get(url, headers=headers)

    return response.json()
