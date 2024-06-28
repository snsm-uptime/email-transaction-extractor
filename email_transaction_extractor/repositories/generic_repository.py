# email_transaction_extractor/repositories/generic_repository.py
from sqlite3 import IntegrityError
from typing import Type, Generic, List, Optional
from sqlalchemy.orm import Session
from email_transaction_extractor.typing import ModelType


class GenericRepository(Generic[ModelType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def create(self, obj_in: ModelType) -> ModelType:
        try:
            self.db.add(obj_in)
            self.db.commit()
            self.db.refresh(obj_in)
            return obj_in
        except IntegrityError as e:
            self.db.rollback()
            raise e

    def get(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[ModelType]:
        return self.db.query(self.model).all()

    def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        db_obj = self.get(id)
        if db_obj:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> Optional[ModelType]:
        db_obj = self.get(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
        return db_obj
