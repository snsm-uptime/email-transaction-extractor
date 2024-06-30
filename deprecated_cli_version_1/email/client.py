import imaplib
import logging
from ..models import ImapServer


class EmailClient:
    def __init__(self, username: str, password: str, imap_server: ImapServer, custom_server: str = None):
        self.username = username
        self.password = password
        self.imap_server = custom_server if imap_server == ImapServer.CUSTOM else imap_server
        self.connection: imaplib.IMAP4_SSL = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def authenticate(self):
        try:
            self.connection = imaplib.IMAP4_SSL(self.imap_server.value)
            self.connection.login(self.username, self.password)
            self.logger.info(
                "Successfully authenticated and connected to the server.")
        except imaplib.IMAP4.error as e:
            self.logger.error(f"Failed to authenticate: {e}")
            raise

    def select_mailbox(self, mailbox: str):
        if not self.connection:
            raise ConnectionError(
                "Not authenticated. Call authenticate() first.")
        self.connection.select(mailbox)
        self.logger.info(f"Mailbox '{mailbox}' selected.")

    def logout(self):
        if self.connection:
            self.connection.logout()
            self.logger.info("Logged out from the server.")
