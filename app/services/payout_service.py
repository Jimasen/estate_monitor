from app.models.bank_account import BankAccount
from app.services.payments.paystack_transfer import (
    create_transfer_recipient,
    transfer_to_bank,
)


def payout_landlord(db, landlord_wallet):

    bank = (
        db.query(BankAccount)
        .filter(BankAccount.user_id == landlord_wallet.user_id)
        .first()
    )

    if not bank:
        raise Exception("Landlord bank account not configured")

    # Create transfer recipient
    recipient = create_transfer_recipient(
        bank.account_name,
        bank.account_number,
        bank.bank_code,
    )

    recipient_code = recipient["data"]["recipient_code"]

    reference = f"payout_{landlord_wallet.user_id}"

    response = transfer_to_bank(
        landlord_wallet.balance,
        recipient_code,
        reference,
    )

    return response
