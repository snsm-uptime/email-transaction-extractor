from abc import ABC, abstractmethod
from datetime import datetime
from email.message import Message
from typing import Protocol


from ..models import ExpensePriority, ExpenseType, Mail, Bank


class HasMessageConstructor(Protocol):
    def __init__(self, msg: Message) -> None:
        ...
