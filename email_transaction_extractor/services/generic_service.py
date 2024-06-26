# email_transaction_extractor/services/generic_service.py
from typing import Type, Generic, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from email_transaction_extractor.typing import ModelType, CreateSchemaType, UpdateSchemaType, ReturnSchemaType
from email_transaction_extractor.repositories.generic_repository import GenericRepository


class GenericService(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReturnSchemaType]):
    def __init__(self, db: Session, model: Type[ModelType], create_schema: Type[CreateSchemaType], update_schema: Type[UpdateSchemaType], return_schema: Type[ReturnSchemaType]):
        self.repository = GenericRepository[ModelType](db, model)
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.return_schema = return_schema

    def create(self, obj_in: CreateSchemaType) -> ReturnSchemaType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db_obj = self.repository.create(db_obj)
        return self.return_schema.model_validate(db_obj)

    def get(self, id: int) -> ReturnSchemaType:
        db_obj = self.repository.get(id)
        return self.return_schema.model_validate(db_obj) if db_obj else None

    def get_all(self) -> List[ReturnSchemaType]:
        db_objs = self.repository.get_all()
        return [self.return_schema.model_validate(obj) for obj in db_objs]

    def update(self, id: int, obj_in: UpdateSchemaType) -> ReturnSchemaType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.repository.update(id, obj_in_data)
        return self.return_schema.model_validate(db_obj) if db_obj else None

    def delete(self, id: int) -> ReturnSchemaType:
        db_obj = self.repository.delete(id)
        return self.return_schema.from_orm(db_obj) if db_obj else None
