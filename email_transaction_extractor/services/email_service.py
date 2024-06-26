from email_transaction_extractor.email.client import EmailClient
from email_transaction_extractor.email.imap_search_criteria import IMAPSearchCriteria
from email_transaction_extractor.models.enums import Bank
from email_transaction_extractor.utils.dates import DateRange


class EmailService:
    def __init__(self, client: EmailClient, range: DateRange):
        self.client = client
        self._default_criteria = IMAPSearchCriteria().date_range(
            range.start_date,
            range.end_date
        )

    def get_mail_from_bank(self, bank: Bank, subject_filter: str | None = None) -> list:
        criteria = self._default_criteria.from_(
            bank.value).subject(subject_filter)
        ids = self.client.fetch_email_ids(criteria)
        emails = self.client.get_emails(ids)
        return emails
