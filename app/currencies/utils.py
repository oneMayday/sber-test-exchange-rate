from .exceptions import CurrencyCodeValidationException


async def validate_currency_code(currency_code: str):
    if len(currency_code) != 3 or not currency_code.isalpha():
        raise CurrencyCodeValidationException
    return currency_code.lower()
