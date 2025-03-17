from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from api.repository import RollRepository
from api.schemas import convert_model, Roll, RollCreate, Statistics
from core.models import RollModel


class RollService:

    __slots__ = ('session', 'repository')

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = RollRepository(self.session)

    async def create(self, data: RollCreate) -> Roll:
        created_roll = await self.repository.create_roll(data)
        return convert_model(Roll, created_roll)

    async def get_list(
        self,
        filters: dict[str, str | int] | None = None
    ) -> list[Roll]:
        if filters is None:
            rolls = await self.repository.get_rolls()
        else:
            rolls = await self.repository.get_rolls_with_filters(filters)
        return convert_model(Roll, rolls, True)

    async def _get_by_id_or_404(self, roll_id: int) -> RollModel:
        try:
            return await self.repository.get_roll_by_id(roll_id)
        except NoResultFound:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

    async def delete(self, roll_id: int) -> Roll:
        roll = await self._get_by_id_or_404(roll_id)
        if roll.deletion_date is not None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Рулон уже удалён.'
            )
        deleted_roll = await self.repository.set_deletion_date(roll)
        return convert_model(Roll, deleted_roll)

    async def get_statistics(
        self,
        from_date: datetime,
        to_date: datetime
    ):
        stats = await self.repository.get_statistics(from_date, to_date)
        print(stats)
        return Statistics(**stats)
