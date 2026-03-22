# app/services/payment_gateway.py

import uuid

from app.services.payments.flutterwave_service import create_payment as flutterwave_create
from app.services.payments.paystack_service import create_payment as paystack_create


# ---------------------------------------------------
# Generate Payment Reference
# ---------------------------------------------------
def generate_reference(prefix="PAY"):

    return f"{prefix}-{uuid.uuid4().hex[:12]}"


# ---------------------------------------------------
# Create Payment (Gateway Switch)
# ---------------------------------------------------
def create_payment_reference(payment, gateway="paystack"):

    reference = generate_reference()

    amount = payment.amount

    email = getattr(payment, "email", "customer@email.com")

    redirect_url = "https://yourdomain.com/payment/complete"

    if gateway == "paystack":

        response = paystack_create(
            amount,
            email,
            reference,
            redirect_url
        )

    elif gateway == "flutterwave":

        response = flutterwave_create(
            amount,
            email,
            reference,
            redirect_url
        )

    else:

        raise Exception("Unsupported payment gateway")

    payment.reference = reference
    payment.gateway = gateway

    return response
