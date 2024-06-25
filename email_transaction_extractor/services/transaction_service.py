from sqlalchemy.orm import Session
from email_transaction_extractor.repositories.transaction_repository import TransactionRepository
from email_transaction_extractor.models.transaction import TransactionTable
from email_transaction_extractor.schemas.transaction import TransactionCreate


class TransactionService:
    def __init__(self, db: Session):
        self.transaction_repository = TransactionRepository(db)

    def create_transaction(self, transaction_data: TransactionCreate):
        transaction = TransactionTable(**transaction_data.model_dump())
        return self.transaction_repository.create(transaction)

    def get_transaction(self, transaction_id: int):
        return self.transaction_repository.get(transaction_id)

    def get_all_transactions(self):
        return self.transaction_repository.get_all()

    def update_transaction(self, transaction_id: int, transaction_data: dict):
        return self.transaction_repository.update(transaction_id, transaction_data)

    def delete_transaction(self, transaction_id: int):
        return self.transaction_repository.delete(transaction_id)
