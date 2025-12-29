import time
from datetime import datetime, timezone
from app.db.session import SessionLocal
from app.db.models import Transaction

def process_transaction(payload):
    db = SessionLocal()
    try:
        txn = db.query(Transaction).filter(
            Transaction.transaction_id == payload.transaction_id
        ).first()

        if txn and txn.status == "PROCESSED":
            return

        if not txn:
            txn = Transaction(
                transaction_id=payload.transaction_id,
                source_account=payload.source_account,
                destination_account=payload.destination_account,
                amount=payload.amount,
                currency=payload.currency,
                status="PROCESSING",
                processed_at=None   
            )
            db.add(txn)
            db.commit()
            db.refresh(txn)

        time.sleep(30)

        txn.status = "PROCESSED"
        txn.processed_at = datetime.now(timezone.utc)

        db.commit()

    finally:
        db.close()
