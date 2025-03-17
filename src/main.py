from fastapi import FastAPI
import uvicorn

from api import api_router
from settings.config import settings


app = FastAPI(debug=settings.debug)
app.include_router(api_router, prefix='/rolls')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='0.0.0.0')
