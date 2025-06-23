async def validate_currency_code(currency_code: str):
    if len(currency_code) != 3 or not currency_code.isalpha():
        raise ValueError("Код валюты должен состоять из 3 буквенных символов")
    return currency_code.lower()
