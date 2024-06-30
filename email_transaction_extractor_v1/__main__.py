import copy
from datetime import UTC, datetime

from sqlalchemy import create_engine

from email_transaction_extractor.database.tables.transaction import TransactionTable
from email_transaction_extractor.models.enums import Bank, ExpensePriority, ExpenseType
from .database.repositories import SQLiteRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, load_only
from contextlib import contextmanager
from typing import List


def main():
    repo = SQLiteRepository('sqlite.db')

    transactions = repo.get_all_transactions()
    for transaction in transactions:
        print(transaction.value)


if __name__ == '__main__':
    main()
