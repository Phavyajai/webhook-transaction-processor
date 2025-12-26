from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    status: str
    created_at: datetime
    processed_at: Optional[datetime]

    class Config:
        orm_mode = True
