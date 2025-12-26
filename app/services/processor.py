import time
from datetime import datetime
from app.db.session import SessionLocal
from app.db.models import Transaction

def process_transaction(transaction_id: str):
    time.sleep(30)  # simulate delay

    db = SessionLocal()
    try:
        txn = db.query(Transaction).filter(
            Transaction.transaction_id == transaction_id
        ).first()

        if txn:
            txn.status = "PROCESSED"
            txn.processed_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()