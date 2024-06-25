from logging import getLogger
from typing import List

from ..email.client import EmailClient
from ..email import (BACMailParser, IMAPSearchCriteria, PromericaMailParser,
                     from_mail_to_transaction)
from ..models import Bank, CLIOptions, Mail, Report, Transaction, TransactionMail
from .email_service import EmailService


class TransactionReport(Report[TransactionMail, Transaction]):
    def __init__(self, options: CLIOptions):
        self.opts = options
        self.email_service = EmailService[Mail](
            client=EmailClient(
                options.user,
                options.password,
                options.imap_server,
                options.custom_server
            ),
            type=Mail
        )
        super().__init__(self.__class__.__name__,
                         options.output_format, getLogger(self.__class__.__name__))

    def get_default_criteria(self, bank: Bank) -> IMAPSearchCriteria:
        return IMAPSearchCriteria().date_range(
            self.opts.date_range.start_date,
            self.opts.date_range.end_date
        ).from_(bank.value)

    def get_mail(self, bank: Bank, subject_filter: str = None) -> List[Mail]:
        criteria = self.get_default_criteria(bank).subject(subject_filter)
        email_ids = self.email_service.fetch_email_ids(
            self.opts.mailbox, criteria)
        emails = self.email_service.fetch_email_details(email_ids)
        return emails

    def mail_parser(self, mail: Mail) -> TransactionMail:
        match mail.author:
            case Bank.PROMERICA.value:
                return PromericaMailParser(mail.msg)
            case Bank.BAC.value:
                return BACMailParser(mail.msg)
            case _:
                self.logger.error(f"Unsupported bank author: {mail.author}")

    def fetch_content(self) -> List[Mail]:
        promerica_emails = self.get_mail(Bank.PROMERICA, 'Comprobante')
        # all messages from this bac email are transaction emails
        bac_emails = self.get_mail(Bank.BAC)
        bac_emails.extend(promerica_emails)
        return [self.mail_parser(m) for m in bac_emails]

    def prepare_content(self, content: List[TransactionMail]) -> List[Transaction]:
        transactions = []
        for mail in content:
            if isinstance(mail, Mail):
                transaction = from_mail_to_transaction(mail=mail)
                transactions.append(transaction)
        return transactions
