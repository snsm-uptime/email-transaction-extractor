from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from email.header import decode_header
from email.message import Message
from enum import Enum, auto
from typing import Protocol

from bs4 import BeautifulSoup

from ..utils.regex import extract_email


class Mail(ABC):
    def __init__(self, msg: Message):
        decoded_header = decode_header(msg.get('subject'))

        normalized_subject = ""
        for part, encoding in decoded_header:
            if isinstance(part, bytes):
                if encoding is None:
                    encoding = "utf-8"
                normalized_subject += part.decode(encoding, errors="replace")
            else:
                normalized_subject += part

        self.subject = normalized_subject
        self.recipient = extract_email(msg.get('from'))
        self.body = self.__get_body(msg)
        self.date = msg.get('date')

    def __get_body(self, msg: Message):
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True)
                        charset = part.get_content_charset()
                        if charset is None:
                            charset = "utf-8"
                        body = body.decode(charset, errors="replace")
                        if content_type == "text/plain":
                            return body
                        elif content_type == "text/html":
                            soup = BeautifulSoup(body, "html.parser")
                            return soup.get_text()
                    except:
                        pass
        else:
            content_type = msg.get_content_type()
            body = msg.get_payload(decode=True)
            charset = msg.get_content_charset()
            if charset is None:
                charset = "utf-8"
            body = body.decode(charset, errors="replace")
            if content_type == "text/plain":
                return body
            elif content_type == "text/html":
                soup = BeautifulSoup(body, "html.parser")
                return soup.get_text()
        return ""

    def __str__(self):
        return f"Subject: {self.subject}\nRecipient: {self.recipient}\nDate: {self.date}\nBody: {self.body}\n"


class ExpenseType(Enum):
    TAXES = auto()
    GROCERIES = auto()
    EATING_OUT = auto()
    ENTERTAINMENT = auto()
    TRANSPORT = auto()
    SELF_CARE = auto()
    PET = auto()
    GIFT = auto()


class ExpensePriority(Enum):
    MUST = auto()
    WANT = auto()
    NEED = auto()


class TransactionDetails:
    value: float
    business: str
    business_type: str
    transaction_type: ExpensePriority
    expense_type: ExpenseType
    date: str
    currency: str


class TransactionMail(Protocol):
    def get_body(self) -> str: ...
    def get_business(self) -> str: ...
    def get_business_type(self) -> str | None: ...
    def get_value_and_currency(self) -> tuple[str, float]: ...
    def get_date(self) -> datetime: ...
    def get_expense_type(self) -> ExpenseType | None: ...
    def get_expense_priority(self) -> ExpensePriority | None: ...


class Banks(Enum):
    PROMERICA = auto()
    BAC = auto()
    SIMAN = auto()


@dataclass
class Transaction:
    body: str
    business: str
    business_type: str | None
    currency: str
    date: datetime
    expense_type: ExpenseType | None
    expense_priority: ExpensePriority | None
    value: float
    bank: Banks
