from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from email_transaction_extractor.models.enums import Bank, ExpensePriority, ExpenseType


class TransactionBase(BaseModel):
    date: datetime
    value: float
    currency: str
    business: str
    business_type: Optional[str] = None
    bank: Bank
    expense_priority: Optional[ExpensePriority] = None
    expense_type: Optional[ExpenseType] = None
    body: str


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True
