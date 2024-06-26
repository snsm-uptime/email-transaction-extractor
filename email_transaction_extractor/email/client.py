import email
import imaplib
import logging
from email.message import Message
from typing import List, Optional

from email_transaction_extractor.email.imap_search_criteria import \
    IMAPSearchCriteria


class EmailClient:
    def __init__(self, email_user: str, email_pass: str, server: str, mailbox: str = "inbox"):
        self.server = server
        self.email_user = email_user
        self.email_pass = email_pass
        self.mailbox = mailbox
        self.connection: Optional[imaplib.IMAP4_SSL] = None
        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.connection = imaplib.IMAP4_SSL(self.server)
        self.connection.login(self.email_user, self.email_pass)
        self.connection.select(self.mailbox)

    def fetch_email_ids(self, criteria: IMAPSearchCriteria) -> Optional[List[str]]:
        status, data = self.connection.search(None, criteria.build())
        if status == 'OK':
            return data[0].split()
        self.logger.error(f'Status not OK {status}')
        return None

    def get_emails(self, email_ids: List[str]) -> List[Message]:
        emails: List[Message] = []
        for email_id in email_ids:
            status, msg_data = self.connection.fetch(email_id, "(RFC822)")
            if status != 'OK':
                self.logger.error(f'Failed to get email with ID {email_id}')
                continue
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    emails.append(msg)
        return emails

    def disconnect(self):
        if self.connection:
            self.connection.logout()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
