from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.services import RollService
from api.schemas import Roll, RollCreate, RollRangeFilters, Statistics
from settings.db_settings import db_helper

router = APIRouter(tags=['rolls'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    summary='Добавляет рулон в хранилище и ставит метку времени добавления.'
)
async def add_roll(
    roll_data: RollCreate,
    session: AsyncSession = Depends(db_helper.get_session)
) -> Roll:
    return await RollService(session).create(roll_data)


@router.post(
    '/list',
    summary='Выводит список рулонов с возможной фильтрацией.'
)
async def get_rolls_list(
    filters: RollRangeFilters | None = None,
    session: AsyncSession = Depends(db_helper.get_session)
) -> list[Roll]:
    return await RollService(session).get_list(
        filters.model_dump(exclude_none=True) if filters else None
    )


@router.delete(
    '/{roll_id}',
    summary='Ставит метку времени на выбранный рулон.'
)
async def set_deletion_date_by_id(
    roll_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
) -> Roll:
    return await RollService(session).delete(roll_id)


@router.get(
    '/statistics',
    summary='Выводит статистику по рулонам за выбранный период.'
)
async def get_stats_for_period(
    from_date: datetime,
    to_date: datetime,
    session: AsyncSession = Depends(db_helper.get_session),
) -> Statistics:
    return await RollService(session).get_statistics(from_date, to_date)
