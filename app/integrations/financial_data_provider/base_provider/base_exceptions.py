from app.utils import BaseCustomException


class FinancialDataProviderResponseException(BaseCustomException):
    default_message = "Ошибка при получении данных от провайдера"
    default_status = 502
