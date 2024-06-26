from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from email_transaction_extractor.models.enums import Bank, ExpensePriority, ExpenseType


class TransactionBase(BaseModel):
    bank: Bank
    body: str
    currency: str
    date: datetime
    value: float

    business: Optional[str] = None
    business_type: Optional[str] = None
    expense_priority: Optional[ExpensePriority] = None
    expense_type: Optional[ExpenseType] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )
