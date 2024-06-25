from sqlalchemy import Column, DateTime, Float, Integer, String, Enum, Text
from datetime import datetime, timezone

from ..database import Base
from ..models.enums import Bank, ExpensePriority, ExpenseType


class TransactionTable(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    value = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    business = Column(String, nullable=False)
    business_type = Column(String, nullable=True)
    bank = Column(Enum(Bank), nullable=False)
    expense_priority = Column(Enum(ExpensePriority), nullable=True)
    expense_type = Column(Enum(ExpenseType), nullable=True)
    body = Column(Text, nullable=False)
