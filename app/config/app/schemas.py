from pydantic import BaseModel


class AppConfig(BaseModel):
    """Базовая схема конфигурации приложения."""
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    title: str = ""
    debug: bool = False


class ApiConfig(BaseModel):
    """Базовая конфигурация API приложения."""
    prefix: str = '/api'
