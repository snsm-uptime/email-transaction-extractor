import re
from datetime import datetime
from typing import Generator, List

from ..models.transactions import Transaction
from ..models.email import Mail, TransactionMail


class MailFilterBuilder:
    def __init__(self, email_list: List[Mail]):
        self.__email_list: List[Mail] = email_list

    def filter_by_authors(self, authors: List[str]) -> 'MailFilterBuilder':
        self.__email_list = list(self.__filter_by_authors(authors))
        return self

    def filter_by_subject_like(self, subject_keyword: str) -> 'MailFilterBuilder':
        self.__email_list = list(
            self.__filter_by_subject_like(subject_keyword))
        return self

    def __filter_by_authors(self, authors: List[str]) -> Generator[Mail, None, None]:
        return (email for email in self.__email_list if email.author in authors)

    def __filter_by_subject_like(self, subject_keyword: str) -> Generator[Mail, None, None]:
        keyword_lower = subject_keyword.lower()
        return (email for email in self.__email_list if keyword_lower in email.subject.lower())

    def filter(self) -> List[Mail]:
        return self.__email_list


class IMAPSearchCriteria:
    def __init__(self):
        self.criteria = []

    def from_(self, email):
        self.criteria.append(f'FROM "{email}"')
        return self

    def to(self, email):
        self.criteria.append(f'TO "{email}"')
        return self

    def cc(self, email):
        self.criteria.append(f'CC "{email}"')
        return self

    def subject(self, subject):
        if subject:
            self.criteria.append(f'SUBJECT "{subject}"')
        return self

    def body(self, text):
        self.criteria.append(f'BODY "{text}"')
        return self

    def date_range(self, start_date: datetime, end_date: datetime):
        start = start_date.strftime("%d-%b-%Y")
        end = end_date.strftime("%d-%b-%Y")
        self.criteria.append(f'SINCE "{start}" BEFORE "{end}"')
        return self

    def unseen(self):
        self.criteria.append('UNSEEN')
        return self

    def deleted(self):
        self.criteria.append('DELETED')
        return self

    def draft(self):
        self.criteria.append('DRAFT')
        return self

    def flagged(self):
        self.criteria.append('FLAGGED')
        return self

    def recent(self):
        self.criteria.append('RECENT')
        return self

    def all(self):
        self.criteria.append('ALL')
        return self

    def and_(self, *criteria):
        combined = ' '.join(f'({c})' for c in criteria)
        self.criteria.append(f'({combined})')
        return self

    def or_(self, *criteria):
        combined = ' '.join(criteria)
        self.criteria.append(f'(OR {combined})')
        return self

    def not_(self, criterion):
        self.criteria.append(f'(NOT {criterion})')
        return self

    def build(self):
        return ' '.join(self.criteria)


def from_mail_to_transaction(mail: TransactionMail) -> Transaction:
    currency, value = mail.get_value_and_currency()
    transaction = Transaction(
        bank=mail.bank,
        body=mail.get_body(),
        business=mail.get_business(),
        business_type=mail.get_business_type(),
        currency=currency,
        date=mail.get_date(),
        expense_priority=mail.get_expense_priority(),
        expense_type=mail.get_expense_type(),
        value=value
    )
    return transaction
