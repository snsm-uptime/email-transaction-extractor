from datetime import date, datetime
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from email_transaction_extractor import config
from email_transaction_extractor.database import get_db
from email_transaction_extractor.email.client import EmailClient
from email_transaction_extractor.schemas.request import RefreshTransactionsRequest
from email_transaction_extractor.schemas.transaction import Transaction, TransactionCreate
from email_transaction_extractor.services.transaction_service import TransactionService
from email_transaction_extractor.utils.dates import DateRange

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/transactions/refresh")
def refresh_transactions_by_date(request: RefreshTransactionsRequest, db: Session = Depends(get_db)):
    """
    Create transactions based on the start date provided in the request.

    Args:
        request: RefreshTransactionsRequest object containing the start date.
        db: Database session.

    Raises:
        HTTPException: If the start date is in the future.

    Returns:
        None
    """
    service = TransactionService(db)
    today = datetime.now()

    if request.start_date > today:
        raise HTTPException(
            status_code=400, detail="Start date cannot be in the future")

    if request.end_date > today:
        request.end_date = today

    date_range = DateRange(request.start_date, request.end_date)

    with EmailClient(
        email_user=config.EMAIL_USER,
        email_pass=config.EMAIL_PASSWORD,
        server=config.EMAIL_SERVER,
        mailbox=config.EMAIL_MAILBOX
    ) as email_client:
        logger.info(
            f"Starting transaction creation process for date range: {date_range}")
        service.refresh_database_with_emails_from_date(
            email_client,
            date_range
        )


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
