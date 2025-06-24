from typing import NoReturn

from sqlalchemy.ext.asyncio import AsyncSession

from ..model_services import CurrencyModelService


class CurrencyGetUniqueCodesUseCase:
    """Получение списка уникальных кодов валют."""
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.currency_model_service = CurrencyModelService(self.session)

    async def execute(self) -> list[str] | NoReturn:
        return await self.currency_model_service.get_unique_currency_codes()
