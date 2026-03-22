import os
import requests


PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET_KEY")


def create_transfer_recipient(name, account_number, bank_code):

    url = "https://api.paystack.co/transferrecipient"

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET}",
        "Content-Type": "application/json",
    }

    payload = {
        "type": "nuban",
        "name": name,
        "account_number": account_number,
        "bank_code": bank_code,
        "currency": "NGN",
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()


def transfer_to_bank(amount, recipient_code, reference):

    url = "https://api.paystack.co/transfer"

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET}",
        "Content-Type": "application/json",
    }

    payload = {
        "source": "balance",
        "amount": int(amount * 100),
        "recipient": recipient_code,
        "reference": reference,
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()
