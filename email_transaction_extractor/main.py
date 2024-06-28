from datetime import datetime, timedelta
import logging
from contextlib import asynccontextmanager
import os

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from sqlalchemy.orm import Session

from email_transaction_extractor import config
from email_transaction_extractor.utils.dates import DateRange

from .database import Base, engine, get_db
from .email import EmailClient
from .routers import transactions
from .services.transaction_service import TransactionService
from .utils.logging import configure_root_logger


def process_emails(db: Session):
    logger = logging.getLogger('process_emails')
    try:
        email_client = EmailClient(
            config.EMAIL_USER,
            config.EMAIL_PASSWORD,
            config.EMAIL_SERVER,
            config.EMAIL_MAILBOX
        )
        transaction_service = TransactionService(db)
        today = datetime.now()
        transactions = transaction_service.get_transactions_from_email_by_date(
            email_client,
            DateRange(
                today - timedelta(minutes=config.REFRESH_INTERVAL_IN_MINUTES),
                today
            )
        )
        for obj in transactions:
            transaction_service.create(obj)
        logger.info("Emails processed successfully.")
    except Exception as e:
        logger.exception(f"Error processing emails: {e}")


def check_emails():
    logger = logging.getLogger('check_emails')
    db: Session = next(get_db())
    try:
        process_emails(db)
    except Exception as e:
        logger.error(f"Error in check_emails: {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    try:
        configure_root_logger(
            log_level=logging.INFO,
            log_file=os.getenv('LOG_FILE', 'app.log')
        )
    except Exception as e:
        logging.error(f"Error configuring logger: {e}")
        raise

    logger = logging.getLogger('lifespan')
    check_emails()
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(check_emails, 'interval', minutes=config.REFRESH_INTERVAL_IN_MINUTES)
    # scheduler.start()
    logger.info("Scheduler started.")
    yield
    # scheduler.shutdown()
    logger.info("Scheduler shutdown.")

app = FastAPI(lifespan=lifespan)
app.include_router(transactions.router)

# TODO: Include "Pago de tarjeta" emails from Promerica
