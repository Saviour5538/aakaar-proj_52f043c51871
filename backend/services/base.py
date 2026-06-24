from typing import Type, TypeVar, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseService:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, obj_in: dict) -> ModelType:
        try:
            obj = self.model(**obj_in)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Error creating {self.model.__name__}: {str(e)}")

    def read(self, db: Session, id: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def update(self, db: Session, id: str, obj_in: dict) -> Optional[ModelType]:
        try:
            obj = db.query(self.model).filter(self.model.id == id).first()
            if not obj:
                return None
            for key, value in obj_in.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Error updating {self.model.__name__}: {str(e)}")

    def delete(self, db: Session, id: str) -> bool:
        try:
            obj = db.query(self.model).filter(self.model.id == id).first()
            if not obj:
                return False
            db.delete(obj)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Error deleting {self.model.__name__}: {str(e)}")

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()