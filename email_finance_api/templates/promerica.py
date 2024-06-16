from dataclasses import asdict
from datetime import datetime
from email.message import Message
from functools import cached_property
import re
from ..models import Banks, ExpenseType, Mail, Transaction, TransactionMail, ExpensePriority


class PromericaMail(Mail, TransactionMail):
    def __init__(self, msg: Message):
        super().__init__(msg)

    @cached_property
    def transaction(self) -> Transaction:
        currency, value = self.get_value_and_currency()
        return Transaction(
            bank=Banks.PROMERICA,
            body=self.get_body(),
            business=self.get_business(),
            business_type=self.get_business_type(),
            currency=currency,
            date=self.get_date(),
            expense_priority=self.get_expense_priority(),
            expense_type=self.get_expense_type(),
            value=value
        )

    def get_value_and_currency(self) -> tuple[str, float]:
        value_currency_match = re.search(
            r"Monto\s+\n (\w+): ([\d,]+.\d{2})", self.body)
        if value_currency_match:
            currency = value_currency_match.group(1)
            value = float(value_currency_match.group(2).replace(',', ''))
            return currency, value
        else:
            raise ValueError(f'No currency or value found in {self.subject}')

    def get_business_type(self) -> str:
        business_type_match = re.search(
            r"Tipo de Comercio\s+([A-Z\s]+)", self.body)
        return business_type_match.group(1).strip() if business_type_match else None

    def get_business(self) -> str:
        business_match = re.search(r"Comercio\s+([A-Z\s]+)", self.body)
        return business_match.group(1).strip() if business_match else None

    def get_body(self) -> str:
        ...

    def get_date(self) -> datetime:
        date_pattern = r"Fecha/hora\s+(\d{2} \w{3} \d{4} / \d{2}:\d{2})"
        date_match = re.search(date_pattern, self.body)
        date_str = date_match.group(1)
        return datetime.strptime(date_str, "%d %b %Y / %H:%M")

    def get_expense_priority(self) -> ExpensePriority | None:
        ...

    def get_expense_type(self) -> ExpenseType | None:
        ...
