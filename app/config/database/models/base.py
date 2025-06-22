from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class BaseModel(DeclarativeBase):
    """Базовая абстрактная модель для таблиц в БД."""
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(self) -> str:
        return f'{self.__class__.__name__.lower()}s'
