from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.db.models import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.processor import process_transaction
from typing import List

router = APIRouter(prefix="/v1")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhooks/transactions", status_code=202)
def receive_webhook(
    payload: TransactionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    txn = Transaction(
        transaction_id=payload.transaction_id,
        source_account=payload.source_account,
        destination_account=payload.destination_account,
        amount=payload.amount,
        currency=payload.currency,
        status="PROCESSING"
    )

    try:
        db.add(txn)
        db.commit()

        background_tasks.add_task(
            process_transaction,
            payload.transaction_id
        )

    except IntegrityError:
        db.rollback()
        # Duplicate webhook → ignore, still return 202

    return {"message": "accepted"}

@router.get(
    "/transactions/{transaction_id}",
    response_model=List[TransactionResponse]
)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    txn = db.query(Transaction).filter(
        Transaction.transaction_id == transaction_id
    ).first()

    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return [txn]
