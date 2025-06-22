from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    title: str = ""
    debug: bool = False


class ApiConfig(BaseModel):
    prefix: str = '/api'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter="__",
    )

    app: AppConfig = AppConfig()
    api: ApiConfig = ApiConfig()


settings = Settings()
