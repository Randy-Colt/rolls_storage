from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from api import api_router
from settings.config import settings
from settings.db_settings import db_helper
from core.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield

app = FastAPI(lifespan=lifespan, debug=settings.debug)
app.include_router(api_router, prefix='/rolls')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='0.0.0.0')
