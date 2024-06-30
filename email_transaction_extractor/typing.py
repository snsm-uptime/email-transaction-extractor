# email_transaction_extractor/typing.py
from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReturnSchemaType = TypeVar("ReturnSchemaType", bound=BaseModel)
