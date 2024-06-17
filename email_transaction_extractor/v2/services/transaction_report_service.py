from typing import List

import pandas as pd

from ..email.promerica import PromericaMail

from ..authentication.email_client import EmailClient
from ..email.processing import IMAPSearchCriteria, MailFilterBuilder
from ..models import Banks, CLIOptions, Mail, Report, StorageType, Transaction
from ..services.email_service import EmailService


class TransactionReport(Report[Transaction]):
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

    def get_content(self) -> List[Transaction]:
        or_criteria = [IMAPSearchCriteria().from_(author).build()
                       for author in self.opts.filter_accounts.split(' ')]
        criteria = IMAPSearchCriteria().and_(
            IMAPSearchCriteria()
            .date_range(
                self.opts.date_range.start_date,
                self.opts.date_range.end_date)
            .build()
        ).or_(*or_criteria).build()

        email_ids = self.email_service.fetch_email_ids(
            self.opts.mailbox,
            criteria
        )
        emails = self.email_service.fetch_email_details(email_ids)
        transactions: List[Transaction] = []
        # bac_emails = MailFilterBuilder(
        #     emails).filter_by_authors([Banks.BAC.value]).filter()
        # promerica_emails = MailFilterBuilder[BACMail](
        #     emails, type=BACMail).filter_by_authors([Banks.BAC.value]).filter()
        promerica_emails = MailFilterBuilder[PromericaMail](emails, type=PromericaMail).filter_by_subject_like(
            'comprobante').filter_by_authors([Banks.PROMERICA.value]).filter()

        transactions.extend(
            map(lambda mail: mail.transaction, promerica_emails))
        return transactions

    def prepare_content(self, content: List[Transaction]) -> pd.DataFrame:
        # Convert the list of Transaction instances to a DataFrame
        return pd.DataFrame([txn.__dict__ for txn in content])


class TransactionReportService:
    def __init__(self, report: Report):
        self.report = report

    def write_report(self):
        self.report()

    def read_content(self) -> List[Transaction]:
        return self.report.content

    def fetch_content(self) -> List[Transaction]:
        return self.report.get_content()
