from app.utils import BaseCustomException


class FinancialDataProviderResponseException(BaseCustomException):
    default_message = "Error when receiving data from the provider"
    default_status = 502
