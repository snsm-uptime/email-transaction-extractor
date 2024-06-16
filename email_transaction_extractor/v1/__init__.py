# TODO: replicate shared CLI
# authentication
# select a mailbox
#

import email
import imaplib
from datetime import datetime, timedelta
from typing import Generic, List, Type, TypeVar


import pandas as pd
from .models import ExpenseType, Mail, Transaction
from .templates.promerica import PromericaMail

username = "s.m.sebastian.n@gmail.com"
password = "tqxd kruy sepe hvqx"

T = TypeVar('T', bound='Mail')


class Mailbox(Generic[T]):
    def __init__(self, username: str, password: str, mail_box: str, mail_type: Type[T], imap_server="imap.gmail.com"):
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.mail_type = mail_type
        self.mail = imaplib.IMAP4_SSL(imap_server)
        self.mail.login(username, password)
        self.mail.select(mail_box)
        self.__emails: List[T] = self.__fetch_mail()

    @property
    def emails(self) -> List[T]:
        return self.__emails

    def __fetch_mail(self) -> List[T]:
        date = (datetime.now() - timedelta(7)).strftime("%d-%b-%Y")
        # Search for emails from this week (since one week ago)
        _, messages = self.mail.search(None, f'SINCE {date}')
        email_ids = messages[0].split()
        emails: List[T] = []

        for email_id in email_ids:
            _, msg_data = self.mail.fetch(email_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            emails.append(self.mail_type(msg))
        return emails

    def refresh(self):
        self.__emails = self.__fetch_mail()

    def find_by_email(self, email: str) -> List[T]:
        filtered_emails = [
            msg for msg in self.emails if msg.recipient and email == msg.recipient]
        return filtered_emails

    def find_by_subject(self, subject) -> List[T]:
        filtered_emails = [
            msg for msg in self.emails if msg.subject and subject in msg.subject]
        return filtered_emails


class FinanceReport:
    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions

    def persist(self) -> None:
        def clean_whitespace(transaction):
            transaction_dict = transaction.__dict__.copy()
            for key, value in transaction_dict.items():
                if isinstance(value, str):
                    transaction_dict[key] = ' '.join(value.split())
            return transaction_dict
        df = pd.DataFrame([clean_whitespace(t) for t in self.transactions])
        df.to_csv('promerica.csv')


def main():
    # Usage example
    mailbox = Mailbox[PromericaMail](
        username, password, "inbox", PromericaMail)
    promerica_emails = mailbox.find_by_email(
        "info@promerica.fi.cr")
    report = FinanceReport(
        transactions=[m.transaction for m in promerica_emails])
    report.persist()
