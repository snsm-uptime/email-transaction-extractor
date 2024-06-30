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


def check_emails():
    logger = logging.getLogger('check_emails')
    db: Session = next(get_db())
    with EmailClient(
        email_user=config.EMAIL_USER,
        email_pass=config.EMAIL_PASSWORD,
        server=config.EMAIL_SERVER,
        mailbox=config.EMAIL_MAILBOX
    ) as client:
        transaction_service = TransactionService(db)
        today = datetime.now()
        logger.info(f'Starting job to fetch new transaction emails')
        transaction_service.refresh_database_with_emails_from_date(
            client,
            DateRange(
                today - timedelta(minutes=config.REFRESH_INTERVAL_IN_MINUTES),
                today
            )
        )
    logger.info(f'Finished scheduled job: check_emails')
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
    logger.info(
        f'JOB: check_emails set to run every {config.REFRESH_INTERVAL_IN_MINUTES} minutes')
    scheduler.add_job(check_emails, 'interval',
                      minutes=config.REFRESH_INTERVAL_IN_MINUTES)
    scheduler.start()
    logger.info("Scheduler started")
    yield
    scheduler.shutdown()
    logger.info("Scheduler shutdown")

app = FastAPI(lifespan=lifespan)
app.include_router(transactions.router)

# TODO: Include "Pago de tarjeta" emails from Promerica
