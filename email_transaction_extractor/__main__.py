from datetime import UTC, datetime

from email_transaction_extractor.database.models.transaction import Transaction
from email_transaction_extractor.models.enums import Bank, ExpensePriority, ExpenseType
from .database.repositories import SQLiteRepository, PostgresRepository


def main():
    # Example SQLite usage
    sqlite_repo = SQLiteRepository('sqlite.db')
    sqlite_repo.create_tables()
    item = Transaction(
        date=datetime.now(UTC),
        value=10000,
        currency='CRC',
        business='McDonalds',
        business_type='Fast Food',
        bank=Bank.BAC,
        expense_priority=ExpensePriority.WANT,
        expense_type=ExpenseType.EATING_OUT,
        body='sample body of the email',
    )

    sqlite_repo.add_transaction(item)
    print(sqlite_repo.get(1))

    # Example PostgreSQL usage
    db_config = {
        'dbname': 'testdb',
        'user': 'testuser',
        'password': 'testpass',
        'host': 'localhost'
    }
    postgres_repo = PostgresRepository(db_config)
    postgres_repo.add(item)
    print(postgres_repo.get(1))


if __name__ == '__main__':
    main()
