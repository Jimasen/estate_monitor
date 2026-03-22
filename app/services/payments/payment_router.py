# app/services/payments/payment_router.py

import logging

from app.services.payments.paystack_service import create_payment as paystack_create
from app.services.payments.flutterwave_service import create_payment as flutterwave_create


logger = logging.getLogger("payment_router")


# Supported payment gateways
PAYMENT_GATEWAYS = {
    "paystack": paystack_create,
    "flutterwave": flutterwave_create,
}


def create_payment(
    gateway: str,
    amount: float,
    email: str,
    reference: str,
    callback_url: str,
):
    """
    Unified payment initialization across multiple gateways.
    """

    try:

        gateway = gateway.lower().strip()

        if gateway not in PAYMENT_GATEWAYS:
            raise ValueError(f"Unsupported payment gateway: {gateway}")

        logger.info(
            f"Initializing payment | gateway={gateway} | amount={amount} | email={email}"
        )

        service = PAYMENT_GATEWAYS[gateway]

        response = service(
            amount=amount,
            email=email,
            reference=reference,
            callback_url=callback_url,
        )

        logger.info(f"Payment initialized successfully via {gateway}")

        return response

    except Exception as e:

        logger.exception("Payment initialization failed: %s", e)
        raise
