from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.utils import PaginationInput, PaginationResponse


class CurrencyExchangeRate(BaseModel):
    id: int
    code: str
    rate: Decimal
    date: date


class CurrencysExchangeRatesSaveRequestInput(BaseModel):
    date: date


class CurrencyExchangeRatesSaveResponse(BaseModel):
    message: str = "Currency rates saved successfully"


class ExchangeRateDeleteByCodeResponse(BaseModel):
    message: str


class ExchangeRateGetAllDataInput(PaginationInput):
    pass


class ExchangeRateGetAllDataResponse(PaginationResponse):
    items: list[CurrencyExchangeRate]


