from datetime import datetime
from typing import Type, Sequence

from pydantic import BaseModel, PositiveFloat

from settings.db_settings import Base


class RollBase(BaseModel):
    length: PositiveFloat
    weight: PositiveFloat


class RollCreate(RollBase):
    pass


class Roll(RollBase):
    id: int
    addition_date: datetime
    deletion_date: datetime | None = None


class RollRangeFilters(BaseModel):
    id: tuple[int, int] | None = None
    length: tuple[PositiveFloat, PositiveFloat] | None = None
    weight: tuple[PositiveFloat, PositiveFloat] | None = None
    addition_date: tuple[datetime, datetime] | None = None
    deletion_date: tuple[datetime, datetime] | None = None


class Statistics(BaseModel):
    added_count: float
    deleted_count: float
    average_length: float
    average_weight: float
    max_length: float
    max_weight: float
    min_length: float
    min_weight: float
    total_weight: float


def convert_model(
    schema: Type[BaseModel],
    model_objects: Base | Sequence[Base],
    many: bool = False
) -> BaseModel | list[BaseModel]:
    if many:
        return [
            schema.model_validate(model_object, from_attributes=True)
            for model_object in model_objects
        ]
    return schema.model_validate(model_objects, from_attributes=True)
