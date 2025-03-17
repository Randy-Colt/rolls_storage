from datetime import datetime

from sqlalchemy import func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from settings.db_settings import Base


class RollModel(Base):
    '''
    Модель рулона.
    '''

    length: Mapped[float]
    weight: Mapped[float]
    addition_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(True),
        server_default=func.now()
    )
    deletion_date: Mapped[datetime | None] = mapped_column(TIMESTAMP(True))
