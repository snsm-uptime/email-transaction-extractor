from abc import ABC, abstractmethod
from datetime import datetime
from email.message import Message
from typing import Protocol


from ..models import ExpensePriority, ExpenseType, Mail, Bank


class HasMessageConstructor(Protocol):
    def __init__(self, msg: Message) -> None:
        ...


class TransactionMail(Mail):
    def __init__(self, bank: Bank, msg: Message):
        self.bank = bank
        super().__init__(msg)

    @abstractmethod
    def get_body(self) -> str: ...
    @abstractmethod
    def get_business(self) -> str: ...
    @abstractmethod
    def get_business_type(self) -> str | None: ...
    @abstractmethod
    def get_value_and_currency(self) -> tuple[str, float]: ...
    @abstractmethod
    def get_date(self) -> datetime: ...
    @abstractmethod
    def get_expense_type(self) -> ExpenseType | None: ...
    @abstractmethod
    def get_expense_priority(self) -> ExpensePriority | None: ...
