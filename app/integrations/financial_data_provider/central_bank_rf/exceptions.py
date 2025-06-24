from ..base_provider.base_exceptions import FinancialDataProviderResponseException


class CentraBankProviderResponseException(FinancialDataProviderResponseException):
    default_message = "Error when receiving data from the Central Bank of the RF"
