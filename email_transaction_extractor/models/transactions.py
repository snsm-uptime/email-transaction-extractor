from dataclasses import dataclass
from datetime import datetime
from .enums import Banks, ExpensePriority, ExpenseType


@dataclass
class Transaction:
    bank: Banks
    body: str
    business: str
    business_type: str | None
    currency: str
    date: datetime
    expense_priority: ExpensePriority | None
    expense_type: ExpenseType | None
    value: float
