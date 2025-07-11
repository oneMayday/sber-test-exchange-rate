import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from starlette import status

from app.currencies.exceptions import (
    CurrencyCodeValidationException,
    ExchangeRatesAlreadyExistsException
)
from app.integrations import (
    FinancialDataProviderResponseException
)
from app.utils.exceptions import BaseCustomException


logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        ExchangeRatesAlreadyExistsException,
        lambda request, exc: ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={
                "status_code": status.HTTP_400_BAD_REQUEST,
                "detail": exc.message
            }
        )
    )
    app.add_exception_handler(
        FinancialDataProviderResponseException,
        lambda request, exc: ORJSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY, content={
                "status_code": status.HTTP_502_BAD_GATEWAY,
                "detail": exc.message
            }
        )
    )
    app.add_exception_handler(
        CurrencyCodeValidationException,
        lambda request, exc: ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={
                "status_code": status.HTTP_400_BAD_REQUEST,
                "detail": exc.message
            }
        )
    )
    app.add_exception_handler(
        BaseCustomException,
        lambda request, exc: ORJSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY, content={
                "status_code": status.HTTP_502_BAD_GATEWAY,
                "detail": exc.message
            }
        )
    )
    app.add_exception_handler(
        Exception,
        lambda request, exc: ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "detail": "Internal server error"
            }
        )
    )


