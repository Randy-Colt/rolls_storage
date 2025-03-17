from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from settings.config import settings


class DatabaseHelper:
    '''Класс для работы с сессиями.'''

    def __init__(self, db_url: str, echo: bool = False):
        self.engine = create_async_engine(db_url)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            expire_on_commit=False
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        try:
            async with self.session_factory() as session:
                yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


db_helper = DatabaseHelper(settings.db_url)
