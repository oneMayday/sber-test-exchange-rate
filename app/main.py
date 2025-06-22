from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.config.settings import settings
from app.config.database import BaseModel, DatabaseSessionMaker
from app.routers import api_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    session_maker = DatabaseSessionMaker(db_config=settings.db)
    async with session_maker.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield

app = FastAPI(
    title=settings.app.title,
    debug=settings.app.debug,
    lifespan=lifespan
)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )
