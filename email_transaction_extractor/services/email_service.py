from email.message import Message
from typing import List, Optional

from email_transaction_extractor.email import EmailClient, IMAPSearchCriteria
from email_transaction_extractor.models.enums import Bank
from email_transaction_extractor.utils.dates import DateRange


class EmailService:
    def __init__(self, client: EmailClient, date_range: DateRange):
        self.client = client
        self._default_criteria = IMAPSearchCriteria().date_range(
            date_range.start_date,
            date_range.end_date
        )

    def get_mail_from_bank(self, bank: Bank, subject_filter: Optional[str] = None) -> List[Message]:
        criteria = self._default_criteria.from_(bank.value)
        if subject_filter:
            criteria = criteria.subject(subject_filter)
        ids = self.client.fetch_email_ids(criteria)
        if ids is None:
            return []
        emails = self.client.get_emails(ids)
        return emails
