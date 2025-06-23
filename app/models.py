from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    """Базовая модель."""
    __abstract__ = True
