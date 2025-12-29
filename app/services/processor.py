from app.db.session import SessionLocal
from app.db.models import Transaction
from app.schemas.transaction import TransactionCreate

def process_transaction(payload: TransactionCreate):
    db = SessionLocal()
    try:
        # Idempotency check
        existing = db.query(Transaction).filter(
            Transaction.transaction_id == payload.transaction_id
        ).first()

        if existing:
            return

        txn = Transaction(
            transaction_id=payload.transaction_id,
            source_account=payload.source_account,
            destination_account=payload.destination_account,
            amount=payload.amount,
            currency=payload.currency,
            status="processing"
        )

        db.add(txn)
        db.commit()

    finally:
        db.close()
