from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.utils import PaginationInput, PaginationResponse


class ExchangeRateDeleteByCodeResponse(BaseModel):

    message: str


class SaveCurrenciesExchangeRatesRequestInput(BaseModel):
    date: date


class SaveCurrenciesExchangeRatesResponse(BaseModel):
    message: str


class CurrencyExchangeRate(BaseModel):
    id: int
    code: str
    rate: Decimal
    date: date


class ExchangeRateGetAllDataInput(PaginationInput):
    pass


class ExchangeRateGetAllDataResponse(PaginationResponse):
    items: list[CurrencyExchangeRate]
