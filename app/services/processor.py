import time
from app.db.session import SessionLocal
from app.db.models import Transaction

def process_transaction(payload):
    db = SessionLocal()
    try:
        txn = db.query(Transaction).filter(
            Transaction.transaction_id == payload.transaction_id
        ).first()

        # If already processed → idempotency
        if txn and txn.status == "PROCESSED":
            return

        # If not exists → create as PROCESSING
        if not txn:
            txn = Transaction(
                transaction_id=payload.transaction_id,
                source_account=payload.source_account,
                destination_account=payload.destination_account,
                amount=payload.amount,
                currency=payload.currency,
                status="PROCESSING"
            )
            db.add(txn)
            db.commit()

        # ⏱️ SIMULATED PROCESSING TIME
        time.sleep(30)

        # ✅ Final state
        txn.status = "PROCESSED"
        db.commit()

    finally:
        db.close()
