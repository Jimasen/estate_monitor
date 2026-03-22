from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction


def credit_wallet(db, wallet, amount, reference):

    wallet.balance += amount

    tx = WalletTransaction(
        wallet_id=wallet.id,
        amount=amount,
        transaction_type="credit",
        reference=reference,
    )

    db.add(tx)
    db.commit()


def debit_wallet(db, wallet, amount, reference):

    if wallet.balance < amount:
        raise Exception("Insufficient wallet balance")

    wallet.balance -= amount

    tx = WalletTransaction(
        wallet_id=wallet.id,
        amount=amount,
        transaction_type="debit",
        reference=reference,
    )

    db.add(tx)
    db.commit()
