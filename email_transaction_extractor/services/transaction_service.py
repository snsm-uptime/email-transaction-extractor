from typing import List
from sqlalchemy.orm import Session

from email_transaction_extractor.email.client import EmailClient
from email_transaction_extractor.email.imap_search_criteria import IMAPSearchCriteria
from email_transaction_extractor.models.enums import Bank
from email_transaction_extractor.models.transaction import TransactionTable
from email_transaction_extractor.schemas.transaction import (Transaction,
                                                             TransactionCreate,
                                                             TransactionUpdate)
from email_transaction_extractor.services.email_service import EmailService
from email_transaction_extractor.services.generic_service import GenericService
from email_transaction_extractor.utils.dates import DateRange
from email_transaction_extractor.utils.parsers.bac_parser import BacMessageParser
from email_transaction_extractor.utils.parsers.promerica_parser import PromericaMessageParser


class TransactionService(GenericService[TransactionTable, TransactionCreate, TransactionUpdate, Transaction]):
    def __init__(self, db: Session):
        super().__init__(db, TransactionTable,
                         TransactionCreate, TransactionUpdate, Transaction)

    def get_transactions_from_email_by_date(self, client: EmailClient, date_range: DateRange) -> List[TransactionCreate]:
        with client:
            service = EmailService(
                client,
                default_criteria=IMAPSearchCriteria().date_range(
                    date_range.start_date,
                    date_range.end_date
                )
            )
            bac_emails = service.get_mail_from_bank(Bank.BAC)
            promerica_emails = service.get_mail_from_bank(
                Bank.PROMERICA, 'Comprobante')
            transactions: list[TransactionCreate] = []

            for email in bac_emails:
                parser = BacMessageParser(email)
                value, currency = parser.parse_value_and_currency()
                transaction = TransactionCreate(
                    date=parser.parse_date(),
                    value=value,
                    currency=currency,
                    business=parser.parse_business(),
                    business_type=parser.parse_business_type(),
                    bank=Bank.BAC,
                    body=parser.body,
                    expense_priority=None,
                    expense_type=None
                )
                transactions.append(transaction)

            for email in promerica_emails:
                parser = PromericaMessageParser(email)
                value, currency = parser.parse_value_and_currency()
                transaction = TransactionCreate(
                    date=parser.parse_date(),
                    value=value,
                    currency=currency,
                    business=parser.parse_business(),
                    business_type=parser.parse_business_type(),
                    bank=Bank.PROMERICA,
                    body=parser.body,
                    expense_priority=None,
                    expense_type=None
                )
                transactions.append(transaction)
            return transactions
