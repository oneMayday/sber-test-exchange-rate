from pydantic_settings import BaseSettings, SettingsConfigDict

from .app import (
    AppConfig,
    ApiConfig
)
from .database import (
    DatabaseConfig
)


class Settings(BaseSettings):
    """Класс настроек проекта."""
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter="__",
    )

    app: AppConfig = AppConfig()
    api: ApiConfig = ApiConfig()
    db: DatabaseConfig = DatabaseConfig()


settings = Settings()
