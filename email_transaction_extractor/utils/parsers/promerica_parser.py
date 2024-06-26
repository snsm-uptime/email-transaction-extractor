import re
from email.message import Message
from typing import Tuple

from email_transaction_extractor.utils import (BaseMessageParser,
                                               strip_excess_whitespace)


class PromericaMessageParser(BaseMessageParser):
    def __init__(self, msg: Message):
        self.msg = msg
        super().__init__(msg)

    def parse_business(self) -> str | None:
        business_match = re.search(r"Comercio\s+([A-Z\s]+)", self.body)
        business = business_match.group(1).strip()
        return ', '.join(strip_excess_whitespace(business)) if business_match else None

    def parse_business_type(self) -> str | None:
        business_type_match = re.search(
            r"Tipo de Comercio\s+([A-Z\s]+)", self.body)
        business_type = business_type_match.group(1).strip()
        return ', '.join(strip_excess_whitespace(business_type)) if business_type_match else None

    def parse_value_and_currency(self) -> Tuple[float, str]:
        value_currency_match = re.search(
            r"Monto\s+\n (\w+): ([\d,]+.\d{2})", self.body)
        if value_currency_match:
            currency = value_currency_match.group(1)
            value = float(value_currency_match.group(2).replace(',', ''))
            return value, currency
        return 0.0, ''
