from app.services.wallet_service import credit_wallet


def record_platform_fee(db, platform_wallet, amount, reference):

    credit_wallet(
        db,
        platform_wallet,
        amount,
        reference,
        "Platform Fee 1%"
    )
