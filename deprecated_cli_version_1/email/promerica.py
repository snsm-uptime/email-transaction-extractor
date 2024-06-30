import re
from datetime import datetime
from dateutil.parser import parse as parse_date
from email.message import Message

import pytz

from ..models import Bank, ExpensePriority, ExpenseType, TransactionMail
from ..utils.decorators import clean_whitespace


class PromericaMailParser(TransactionMail):
    def __init__(self, msg: Message):
        super().__init__(bank=Bank.PROMERICA, msg=msg)

    def get_value_and_currency(self) -> tuple[str, float]:
        value_currency_match = re.search(
            r"Monto\s+\n (\w+): ([\d,]+.\d{2})", self.body)
        if value_currency_match:
            currency = value_currency_match.group(1)
            value = float(value_currency_match.group(2).replace(',', ''))
            return currency, value
        else:
            raise ValueError(f'No currency or value found in {self.subject}')

    @clean_whitespace
    def get_business_type(self) -> str:
        business_type_match = re.search(
            r"Tipo de Comercio\s+([A-Z\s]+)", self.body)
        return business_type_match.group(1).strip() if business_type_match else None

    @clean_whitespace
    def get_business(self) -> str:
        business_match = re.search(r"Comercio\s+([A-Z\s]+)", self.body)
        return business_match.group(1).strip() if business_match else None

    @clean_whitespace
    def get_body(self) -> str:
        return self.body

    def get_date(self) -> datetime:
        date_pattern = r"Fecha/hora\s+(\d{2} \w{3} \d{4} / \d{2}:\d{2})"
        date_match = re.search(date_pattern, self.body)
        date_str = date_match.group(1)
        dt = parse_date(date_str)
        return dt.replace(tzinfo=pytz.UTC)

    def get_expense_priority(self) -> ExpensePriority | None:
        ...

    def get_expense_type(self) -> ExpenseType | None:
        ...
