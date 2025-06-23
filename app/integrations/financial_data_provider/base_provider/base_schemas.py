from datetime import date
from decimal import Decimal

from pydantic import (
    BaseModel,
    Field,
)


class ProviderCurrencyInfo(BaseModel):
    """Информация о валюте от провайдера."""
    code: str = Field(description="Код валюты")
    name: str = Field(description="Название валюты")


class ProviderExchangeRateInfo(BaseModel):
    """Информация о курсе обмена от провайдера."""
    quote_currency_code: str = Field(description="Код котируемой валюты")
    quote_currency_name: str = Field(description="Название котируемой валюты")
    exchange_rate: Decimal = Field(description="Курс обмена")
    base_currency_code: str = Field(description="Код базовой валюты")
    base_currency_name: str = Field(description="Название базовой валюты")
    date: date


class GetExchangeRateProviderRequestParams(BaseModel):
    date: date


class GetExchangeRateLitProviderResponse(BaseModel):
    """Ответ от провайдера."""
    currencies_info: list[ProviderCurrencyInfo | None] = Field(
        description="Список валют",
        default_factory=list
    )
    exchange_rates_info: list[ProviderExchangeRateInfo | None] = Field(
        description="Список курсов обмена",
        default_factory=list
    )
