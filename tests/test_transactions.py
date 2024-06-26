import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from email_transaction_extractor.database import Base
from email_transaction_extractor.models.enums import Bank
from email_transaction_extractor.services.transaction_service import TransactionService
from email_transaction_extractor.schemas.transaction import TransactionCreate
from email_transaction_extractor.email import EmailClient
import email

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_transaction(test_db):
    service = TransactionService(test_db)
    transaction_data = TransactionCreate(
        date="2022-01-01T00:00:00Z",
        value=100.0,
        currency="USD",
        business="Store",
        business_type="Retail",
        bank=Bank.PROMERICA,
        expense_priority=1,
        expense_type=2,
        body="Transaction details"
    )
    transaction = service.create_transaction(transaction_data)
    assert transaction.id is not None


@pytest.mark.skip(reason="not implemented process emails in TransactionService")
def test_process_emails(test_db, monkeypatch):
    def mock_connect(self):
        pass

    def mock_get_emails(self, subject_filter, sender_filter):
        msg_content = """\
From: no-reply@bank.com
Subject: Transaction Report

Date: 2022-01-01
Value: 100.0
Currency: USD
Business: Store
Body: Transaction details
"""
        msg = email.message_from_string(msg_content)
        return [msg]

    def mock_disconnect(self):
        pass

    monkeypatch.setattr(EmailClient, "connect", mock_connect)
    monkeypatch.setattr(EmailClient, "get_emails", mock_get_emails)
    monkeypatch.setattr(EmailClient, "disconnect", mock_disconnect)

    email_reader = EmailClient(
        "fake_user", "fake_pass", "fake_server", "inbox")
    service = TransactionService(test_db)
    service.process_emails(
        email_reader, "Transaction Report", "no-reply@bank.com")

    transactions = service.get_all_transactions()
    assert len(transactions) == 1
    assert transactions[0].business == "Store"
    assert transactions[0].value == 100.0
    assert transactions[0].currency == "USD"
