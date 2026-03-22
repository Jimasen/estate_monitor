from app.models.wallet import Wallet
from app.services.payout_service import payout_landlord


def process_landlord_payouts(db):

    wallets = (
        db.query(Wallet)
        .filter(Wallet.balance > 0)
        .all()
    )

    for wallet in wallets:

        try:

            payout_landlord(db, wallet)

            wallet.balance = 0

            db.commit()

            print(f"Payout sent to landlord {wallet.user_id}")

        except Exception as e:

            print(f"Payout failed {wallet.user_id}: {e}")
