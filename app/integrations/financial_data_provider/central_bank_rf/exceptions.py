from ..base_provider.base_exceptions import FinancialDataProviderResponseException


class CentraBankProviderResponseException(FinancialDataProviderResponseException):
    default_message = "Ошибка при получении данных от ЦБ РФ"
