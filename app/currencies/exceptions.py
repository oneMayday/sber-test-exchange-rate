from app.utils import BaseCustomException


class CurrencyCodeValidationException(BaseCustomException):
    default_message = "The currency code must consist of 3 alphabetic characters"
