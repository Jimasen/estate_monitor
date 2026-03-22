from app.services.escrow_service import create_escrow, release_escrow
from app.services.ledger_service import record_platform_fee


def process_rent_payment(
    db,
    tenant_wallet,
    landlord_wallet,
    platform_wallet,
    amount,
    reference,
):

    # Calculate platform fee
    platform_fee = amount * 0.01

    landlord_amount = amount - platform_fee

    # Record platform fee
    record_platform_fee(
        db,
        platform_wallet,
        platform_fee,
        reference
    )

    # Create escrow for landlord amount
    escrow = create_escrow(
        db,
        tenant_wallet.user_id,
        landlord_wallet.user_id,
        reference,
        landlord_amount,
    )

    # Release escrow automatically
    release_escrow(
        db,
        escrow,
        landlord_wallet,
    )

    return {
        "status": "success",
        "platform_fee": platform_fee,
        "landlord_amount": landlord_amount,
    }
