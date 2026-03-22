from app.models.escrow import Escrow
from app.services.wallet_service import credit_wallet


def create_escrow(db, tenant_id, landlord_id, reference, amount):

    escrow = Escrow(
        tenant_id=tenant_id,
        landlord_id=landlord_id,
        payment_reference=reference,
        amount=amount,
        status="held",
    )

    db.add(escrow)
    db.commit()

    return escrow


def release_escrow(db, escrow, landlord_wallet):

    escrow.status = "released"

    credit_wallet(
        db,
        landlord_wallet,
        escrow.amount,
        f"escrow_release_{escrow.id}",
        "Escrow payout to landlord",
    )

    db.commit()


def refund_escrow(db, escrow, tenant_wallet):

    escrow.status = "refunded"

    credit_wallet(
        db,
        tenant_wallet,
        escrow.amount,
        f"escrow_refund_{escrow.id}",
        "Escrow refund to tenant",
    )

    db.commit()
