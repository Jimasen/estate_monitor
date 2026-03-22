# app/services/payment_gateway/ledger_service.py
from app.database.session import SessionLocal
from app.models.wallet_transaction import WalletTransaction
from datetime import datetime

def credit_platform_fee(user_id: int, amount: float, reference_id: int):
    db = SessionLocal()
    try:
        transaction = WalletTransaction(
            user_id=user_id,
            amount=amount,
            type="credit",
            description=f"1% platform fee for payment {reference_id}",
            created_at=datetime.utcnow()
        )
        db.add(transaction)
        db.commit()
        print(f"[Ledger] Credited 1% fee for user {user_id} - amount {amount}")
    finally:
        db.close()
