from datetime import datetime, timedelta
from .exceptions import TransactionIDExistsError
import logging
from contextlib import asynccontextmanager
import os
from sqlalchemy.exc import IntegrityError

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
    email_client = EmailClient(
        email_user=config.EMAIL_USER,
        email_pass=config.EMAIL_PASSWORD,
        server=config.EMAIL_SERVER,
        mailbox=config.EMAIL_MAILBOX
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
        try:
            logger.info(f'Processing {obj.business}')
            transaction_service.create(obj)
        except TransactionIDExistsError as e:
            logger.info(
                f'Transaction ID already exists for {obj.business}, skipping.')
            # logger.exception(e)
            continue
        except IntegrityError as e:
            logger.error(f'Integrity error while processing {obj.business}')
            # logger.exception(e)
            continue
        except Exception as e:
            logger.error(f'Unexpected error while processing {obj.business}')
            # logger.exception(e)
            continue
    logger.info("Emails processed successfully.")


def check_emails():
    logger = logging.getLogger('check_emails')
    db: Session = next(get_db())
    process_emails(db)
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
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_emails, 'interval',
                      minutes=config.REFRESH_INTERVAL_IN_MINUTES)
    scheduler.start()
    logger.info("Scheduler started.")
    yield
    scheduler.shutdown()
    logger.info("Scheduler shutdown.")

app = FastAPI(lifespan=lifespan)
app.include_router(transactions.router)

# TODO: Include "Pago de tarjeta" emails from Promerica
