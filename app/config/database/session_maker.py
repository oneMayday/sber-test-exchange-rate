from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from .schemas import DatabaseConfig
from app.config.settings import settings


class DatabaseSessionMaker:
    """Класс управления сессиями БД."""
    def __init__(self, db_config: DatabaseConfig):
        self.engine = create_async_engine(
            url=db_config.url,
            echo=db_config.echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=db_config.autoflush,
            autocommit=db_config.autocommit,
            expire_on_commit=db_config.expire_on_commit,
        )

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()


session_maker = DatabaseSessionMaker(db_config=settings.db)
