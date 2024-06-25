from sqlalchemy.orm import Session
from email_transaction_extractor.models.transaction import TransactionTable


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, transaction: TransactionTable):
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get(self, transaction_id: int):
        return self.db.query(TransactionTable).filter(TransactionTable.id == transaction_id).first()

    def get_all(self):
        return self.db.query(TransactionTable).all()

    def update(self, transaction_id: int, transaction_data: dict):
        transaction = self.get(transaction_id)
        if transaction:
            for key, value in transaction_data.items():
                setattr(transaction, key, value)
            self.db.commit()
            self.db.refresh(transaction)
        return transaction

    def delete(self, transaction_id: int):
        transaction = self.get(transaction_id)
        if transaction:
            self.db.delete(transaction)
            self.db.commit()
        return transaction
