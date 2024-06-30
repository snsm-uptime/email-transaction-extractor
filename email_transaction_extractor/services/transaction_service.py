from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from email_transaction_extractor.email.client import EmailClient
from email_transaction_extractor.email.imap_search_criteria import \
    IMAPSearchCriteria
from email_transaction_extractor.exceptions import TransactionIDExistsError
from email_transaction_extractor.models.enums import Bank
from email_transaction_extractor.models.transaction import (
    TransactionTable, generate_transaction_id)
from email_transaction_extractor.schemas.transaction import (Transaction,
                                                             TransactionCreate,
                                                             TransactionUpdate)
from email_transaction_extractor.services.email_service import EmailService
from email_transaction_extractor.services.generic_service import GenericService
from email_transaction_extractor.utils.dates import DateRange
from email_transaction_extractor.utils.parsers.bac_parser import \
    BacMessageParser
from email_transaction_extractor.utils.parsers.promerica_parser import \
    PromericaMessageParser


class TransactionService(GenericService[TransactionTable, TransactionCreate, TransactionUpdate, Transaction]):
    def __init__(self, db: Session):
        super().__init__(db, TransactionTable,
                         TransactionCreate, TransactionUpdate, Transaction)

    def create(self, obj_in: TransactionCreate) -> Transaction:
        transaction_id = generate_transaction_id(
            obj_in.bank, obj_in.value, obj_in.date)
        obj_in_data = obj_in.model_dump()
        obj_in_data['id'] = transaction_id
        obj_in_data['bank'] = obj_in.bank.name
        db_obj = self.repository.model(**obj_in_data)
        try:
            db_obj = self.repository.create(db_obj)
            self.logger.info('Created obj with id' + db_obj.id)
            # TODO: Add bank and bank_email to the transaction model to avoid type missmatch error
        except IntegrityError:
            raise TransactionIDExistsError(transaction_id)
        return self.return_schema.model_validate(db_obj)

    def get_all(self) -> List[Transaction]:
        db_objs = self.repository.get_all()
        # Create a list of transactions without the 'body' field
        transactions_without_body = [
            Transaction(
                id=obj.id,
                date=obj.date,
                value=obj.value,
                currency=obj.currency,
                business=obj.business,
                business_type=obj.business_type,
                bank=obj.bank,
                expense_priority=obj.expense_priority,
                expense_type=obj.expense_type
            )
            for obj in db_objs
        ]
        self.logger.info(
            f'TOTAL TRANSACTIONS: {len(transactions_without_body)}')
        return transactions_without_body

    def refresh_database_with_emails_from_date(self, client: EmailClient, date_range: DateRange):
        transactions = self.get_transactions_from_email_by_date(
            client, date_range)
        new_count = 0
        for obj in transactions:
            try:
                self.logger.info(
                    f'Processing transaction\tday={obj.date.isoformat()}\tbusiness={obj.business}')
                new_count += 1
                self.create(obj)
            except TransactionIDExistsError as e:
                self.logger.info(
                    f'Transaction ID {e.transaction_id} already exists for {obj.business}, skipping.')
                self.logger.exception(e)
                continue
            except IntegrityError as e:
                self.logger.error(
                    f'Integrity error while processing {obj.business}')
                self.logger.exception(e)
                continue
            except Exception as e:
                self.logger.error(
                    f'Unexpected error while processing {obj.business}')
                self.logger.exception(e)
                continue
        self.logger.info(
            f"{len(transactions)} Emails processed successfully. Created {new_count} new entries in the DB")

    def get_transactions_from_email_by_date(self, client: EmailClient, date_range: DateRange) -> List[TransactionCreate]:
        """
        Fetches transaction emails from specified banks within a given date range, parses the emails to extract transaction details,
        and returns a list of TransactionCreate objects.

        Args:
            client (EmailClient): An instance of EmailClient used to connect to the email server and fetch emails.
            date_range (DateRange): An instance of DateRange specifying the start and end dates for fetching emails.

        Returns:
            List[TransactionCreate]: A list of TransactionCreate objects containing the extracted transaction details from the emails.
        """
        service = EmailService(
            client,
            default_criteria=IMAPSearchCriteria().date_range(
                date_range.start_date, date_range.end_date)
        )
        bac_emails = service.get_mail_from_bank(Bank.BAC)
        self.logger.info('Fetched the BAC transaction emails')
        promerica_emails = service.get_mail_from_bank(
            Bank.PROMERICA, 'Comprobante de')
        self.logger.info('Fetched the PROMERICA transaction emails')
        transactions: list[TransactionCreate] = []

        for bank_emails, parser_class in [(bac_emails, BacMessageParser), (promerica_emails, PromericaMessageParser)]:
            for email in bank_emails:
                parser = parser_class(email)
                value, currency = parser.parse_value_and_currency()
                transaction = TransactionCreate(
                    date=parser.parse_date(),
                    value=value,
                    currency=currency,
                    business=parser.parse_business(),
                    business_type=parser.parse_business_type(),
                    bank=Bank.BAC if parser_class == BacMessageParser else Bank.PROMERICA,
                    body=parser.body,
                    expense_priority=None,
                    expense_type=None
                )
                transactions.append(transaction)

        self.logger.info('Extracted transaction details from emails')
        self.logger.info(f'Total transactions = {len(transactions)}')
        return transactions
