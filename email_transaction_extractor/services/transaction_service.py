from sqlalchemy.orm import Session

from email_transaction_extractor.models.transaction import TransactionTable
from email_transaction_extractor.schemas.transaction import (Transaction,
                                                             TransactionCreate,
                                                             TransactionUpdate)
from email_transaction_extractor.services.generic_service import GenericService


class TransactionService(GenericService[TransactionTable, TransactionCreate, TransactionUpdate, Transaction]):
    def __init__(self, db: Session):
        super().__init__(db, TransactionTable,
                         TransactionCreate, TransactionUpdate, Transaction)
