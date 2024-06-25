import copy
from typing import List, Optional
from ._base_repository import BaseRepository
from ..tables.transaction import TransactionTable
from email_transaction_extractor.models import Transaction


class SQLiteRepository(BaseRepository):
    def __init__(self, db_path: str):
        db_url = f'sqlite:///{db_path}'
        super().__init__(db_url)

    def _map_result_to_table_data(self, obj: Transaction) -> TransactionTable:
        """
        Map an SQLAlchemy Transaction model to a dataclass Transaction.

        Args:
            transaction_model (TransactionModel): The SQLAlchemy Transaction model instance.

        Returns:
            Transaction: The dataclass Transaction instance.
        """
        return TransactionTable(
            date=obj.date,
            value=obj.value,
            currency=obj.currency,
            business=obj.business,
            business_type=obj.business_type,
            bank=obj.bank,
            expense_priority=obj.expense_priority,
            expense_type=obj.expense_type,
            body=obj.body
        )

    def _map_result_to_table_data(self, obj: TransactionTable) -> Transaction:
        """
        Map an SQLAlchemy Transaction model to a dataclass Transaction.

        Args:
            transaction_model (TransactionModel): The SQLAlchemy Transaction model instance.

        Returns:
            Transaction: The dataclass Transaction instance.
        """
        return Transaction(
            date=obj.date,
            value=obj.value,
            currency=obj.currency,
            business=obj.business,
            business_type=obj.business_type,
            bank=obj.bank,
            expense_priority=obj.expense_priority,
            expense_type=obj.expense_type,
            body=obj.body
        )

    def add_transaction(self, transaction: TransactionTable) -> None:
        with self.session_scope() as session:
            session.add(transaction)

    def get_all_transactions(self) -> List[Transaction]:
        data = []
        with self.session_scope() as session:
            transaction_table = session.query(TransactionTable).all()
            for transaction in transaction_table:
                obj = self._map_result_to_table_data(transaction)
                data.append(obj)
        return data

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
