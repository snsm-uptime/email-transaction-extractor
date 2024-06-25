from ..tables.transaction import TransactionTable
from ._base_repository import BaseRepository


class PostgresRepository(BaseRepository):
    def __init__(self, db_config: dict):
        db_url = f"postgresql://{db_config['user']}:{
            db_config['password']}@{db_config['host']}/{db_config['dbname']}"
        super().__init__(db_url)
        self.create_tables()

    def add_transaction(self, transaction: TransactionTable) -> None:
        with self.session_scope() as session:
            session.add(transaction)

    def get_transaction(self, transaction_id: int) -> TransactionTable:
        with self.session_scope() as session:
            return session.query(TransactionTable).filter(TransactionTable.id == transaction_id).one_or_none()

    def update_transaction(self, transaction: TransactionTable) -> None:
        with self.session_scope() as session:
            existing_transaction = session.query(TransactionTable).filter(
                TransactionTable.id == transaction.id).one_or_none()
            if existing_transaction:
                existing_transaction.date = transaction.date
                existing_transaction.value = transaction.value
                existing_transaction.currency = transaction.currency
                existing_transaction.business = transaction.business
                existing_transaction.business_type = transaction.business_type
                existing_transaction.bank = transaction.bank
                existing_transaction.expense_priority = transaction.expense_priority
                existing_transaction.expense_type = transaction.expense_type
                existing_transaction.body = transaction.body

    def delete_transaction(self, transaction_id: int) -> None:
        with self.session_scope() as session:
            transaction = session.query(TransactionTable).filter(
                TransactionTable.id == transaction_id).one_or_none()
            if transaction:
                session.delete(transaction)
