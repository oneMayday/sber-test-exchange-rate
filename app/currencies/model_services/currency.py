from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Currency


class CurrencyModelService:
    """Сервис взаимодействия БД с моделью Currency"""
    model = Currency

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self) -> list[Currency]:
        stmt = select(self.model)
        result: Result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_unique_currency_codes(self) -> list[str]:
        stmt = select(self.model.code).order_by(self.model.code)
        result: Result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def save_bulk(self, currencies: list[Currency]):
        self.session.add_all(currencies)
        await self.session.commit()
