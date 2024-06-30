import email
import logging
from typing import Generic, List, Type, TypeVar

from ..email.client import EmailClient
from ..email.processing import IMAPSearchCriteria
from ..models.protocols import HasMessageConstructor

T = TypeVar('T', bound=HasMessageConstructor)


class EmailService(Generic[T]):
    def __init__(self, client: EmailClient, type: Type[T]):
        client.authenticate()
        self.client = client
        self.logger = logging.getLogger(self.__class__.__name__)
        self.type = type

    def fetch_email_ids(self, mailbox: str, criteria: IMAPSearchCriteria) -> list[str] | None:
        self.client.select_mailbox(mailbox)
        status, data = self.client.connection.search(None, criteria.build())
        if status == 'OK':
            return data[0].split()
        self.logger.error(f'Status not OK {status}')

    def fetch_email_details(self, email_ids) -> List[T]:
        emails = []
        for email_id in email_ids:
            # Fetch the email by ID
            status, data = self.client.connection.fetch(email_id, '(RFC822)')
            if status != 'OK':
                self.logger.error(f"Failed to fetch email with ID {email_id}")
                continue
            msg = email.message_from_bytes(data[0][1])
            emails.append(self.type(msg))
        return emails

    def logout(self):
        self.client.connection.logout()
