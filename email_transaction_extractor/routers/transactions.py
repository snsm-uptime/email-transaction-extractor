from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from email_transaction_extractor.database import get_db
from email_transaction_extractor.schemas.transaction import Transaction, TransactionCreate
from email_transaction_extractor.services.transaction_service import TransactionService

router = APIRouter()


@router.post("/transactions/", response_model=Transaction)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.create(transaction)


@router.get("/transactions/{transaction_id}", response_model=Transaction)
def read_transaction(transaction_id: str, db: Session = Depends(get_db)):
    service = TransactionService(db)
    transaction = service.get(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.get("/transactions/", response_model=list[Transaction])
def read_all_transactions(db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.get_all()


@router.put("/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: int, transaction_data: TransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.update_transaction(transaction_id, transaction_data.dict())


@router.delete("/transactions/{transaction_id}", response_model=Transaction)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.delete_transaction(transaction_id)
