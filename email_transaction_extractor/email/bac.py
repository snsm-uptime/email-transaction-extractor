from datetime import datetime
from dateutil.parser import parse as parse_date
from email.message import Message
import re
from typing import Tuple

from ..utils.decorators import clean_whitespace
from ..models import ExpenseType, TransactionMail, ExpensePriority, Bank


class BACMailParser(TransactionMail):
    def __init__(self, msg: Message):
        super().__init__(bank=Bank.BAC, msg=msg)

    @clean_whitespace
    def get_body(self) -> str:
        return self.body

    @clean_whitespace
    def get_business(self) -> str:
        regex = re.compile(
            r'Comercio:\s*\r\n(?P<business>.+?)\s*\n', re.DOTALL)
        match = regex.search(self.body)
        return match.group('business').strip() if match else ''

    def get_business_type(self) -> str | None:
        # Implement this method if necessary, placeholder for now
        return None

    def get_value_and_currency(self) -> Tuple[str, float]:
        regex = re.compile(
            r'Monto:\s*\r\n\s*(?P<currency>\w+)\s(?P<value>[\d,]+\.\d{2})')
        match = regex.search(self.body)
        if match:
            currency = match.group('currency').strip()
            value = float(match.group('value').replace(',', ''))
            return currency, value
        return '', 0.0

    def get_date(self) -> datetime:
        return parse_date(self.date)

    def get_expense_type(self) -> ExpenseType | None:
        # Implement this method if necessary, placeholder for now
        return None

    def get_expense_priority(self) -> ExpensePriority | None:
        # Implement this method if necessary, placeholder for now
        return None
