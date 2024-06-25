from fastapi import FastAPI
from email_transaction_extractor.routers import TransactionRouter
from email_transaction_extractor.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(TransactionRouter)
