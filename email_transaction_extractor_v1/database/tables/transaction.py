from sqlalchemy import Column, DateTime, Float, Integer, String, Enum, Text
from datetime import datetime, UTC

from email_transaction_extractor.models.enums import Bank, ExpensePriority, ExpenseType
from .. import Base


class TransactionTable(Base):
    __tablename__ = 'transactions'

    id = Column(String, primary_key=True)
    date = Column(DateTime, default=datetime.now(UTC))
    value = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    business = Column(String, nullable=False)
    business_type = Column(String, nullable=True)
    bank = Column(Enum(Bank), nullable=False)
    expense_priority = Column(Enum(ExpensePriority), nullable=True)
    expense_type = Column(Enum(ExpenseType), nullable=True)
    body = Column(Text, nullable=False)
