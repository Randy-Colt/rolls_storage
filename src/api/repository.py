from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import case, func, RowMapping, or_, select
from sqlalchemy.sql.elements import Case
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import RollCreate
from core.models import RollModel


class RollRepository:
    '''Репозиторий для CRUD операций с рулоном.'''

    __slots__ = ('session',)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_roll(
        self,
        data: RollCreate
    ) -> RollModel:
        '''Создать рулон по заданным длине и весу.'''
        roll = RollModel(**data.model_dump())
        self.session.add(roll)
        await self.session.commit()
        return roll

    async def get_rolls(self) -> Sequence[RollModel]:
        '''Получить список рулонов без фильтрации.'''
        result = await self.session.execute(select(RollModel))
        return result.scalars().all()

    async def get_rolls_with_filters(
        self,
        filters: dict[str, tuple[str | int]]
    ) -> Sequence[RollModel]:
        '''Получить список рулонов с фильтрацией.'''
        filter_params = (
            getattr(RollModel, param).between(*values)
            for param, values in filters.items()
        )
        query = select(RollModel).where(*filter_params)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_roll_by_id(self, roll_id: int) -> RollModel:
        '''Получить рулон по идентификатору.'''
        return await self.session.get_one(RollModel, roll_id)

    async def set_deletion_date(self, roll: RollModel) -> RollModel:
        '''Установить дату удаления рулона со склада.'''
        roll.deletion_date = func.now()
        await self.session.commit()
        await self.session.refresh(roll, ('deletion_date',))
        return roll

    def __case_for_roll(
        self,
        date_attr: str,
        from_date: datetime,
        to_date: datetime
    ) -> Case[Any]:
        '''Case-функция отбора дат удаления и добавления за заданный период.'''
        return case(
                    (
                        getattr(RollModel, date_attr)
                        .between(from_date, to_date),
                        1
                    ),
                    else_=0
                )

    async def get_statistics(
        self,
        from_date: datetime,
        to_date: datetime
    ) -> RowMapping:
        '''Получить статистику по рулонам за заданный период.'''
        aggregations = (
            func.sum(
                self.__case_for_roll('addition_date', from_date, to_date)
            ).label('added_count'),
            func.sum(
                self.__case_for_roll('deletion_date', from_date, to_date)
            ).label('deleted_count'),
            func.avg(RollModel.length).label('average_length'),
            func.avg(RollModel.weight).label('average_weight'),
            func.max(RollModel.length).label('max_length'),
            func.max(RollModel.weight).label('max_weight'),
            func.min(RollModel.length).label('min_length'),
            func.min(RollModel.weight).label('min_weight'),
            func.sum(RollModel.weight).label("total_weight")
        )
        query = select(*aggregations).where(
            or_(
                    RollModel.addition_date.between(from_date, to_date),
                    RollModel.deletion_date.between(from_date, to_date),
                )
        )
        result = await self.session.execute(query)
        return result.mappings().fetchone()
