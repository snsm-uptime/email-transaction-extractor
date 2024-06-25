from dataclasses import dataclass
from datetime import datetime
from .enums import Bank, ExpensePriority, ExpenseType


@dataclass
class Transaction:
    date: datetime
    value: float
    currency: str
    business: str
    business_type: str | None
    bank: Bank
    expense_priority: ExpensePriority | None
    expense_type: ExpenseType | None
    body: str
