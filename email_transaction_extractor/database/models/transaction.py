from sqlalchemy import Column, DateTime, Float, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, UTC

from email_transaction_extractor.models.enums import Bank, ExpensePriority, ExpenseType

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now(UTC))
    value = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    business = Column(String, nullable=False)
    business_type = Column(String, nullable=True)
    bank = Column(Enum(Bank), nullable=False)
    expense_priority = Column(Enum(ExpensePriority), nullable=True)
    expense_type = Column(Enum(ExpenseType), nullable=True)
    body = Column(Text, nullable=False)
