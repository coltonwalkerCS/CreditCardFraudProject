from typing import Generic, Type, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class BaseRepo(Generic[ModelT]):
    def __init__(self, model: Type[ModelT]):
        self.model = model

    def get_by_id(self, session: Session, entity_id: UUID) -> ModelT | None:
        return session.get(self.model, entity_id)

    def insert(self, session: Session, **kwargs) -> ModelT:
        obj = self.model(**kwargs)
        session.add(obj)
        return obj

    def update(self, obj: ModelT, **kwargs) -> ModelT:
        for k, v in kwargs.items():
            setattr(obj, k, v)
        return obj

    def delete(self, session: Session, obj: ModelT) -> None:
        session.delete(obj)
        session.delete(obj)
