from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    """Базовая схема конфигурации БД."""
    url: str = ""
    echo: bool = False
    autoflush: bool = False
    autocommit: bool = False
    expire_on_commit: bool = False
