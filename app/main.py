from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.handlers import setup_exception_handlers
from app.config.settings import settings
from app.routers import api_router
from app.models import BaseModel


@asynccontextmanager
async def lifespan(_app: FastAPI):
    from app.config.database.session_maker import session_maker

    async with session_maker.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield

app = FastAPI(
    title=settings.app.title,
    debug=settings.app.debug,
    lifespan=lifespan
)

app.include_router(api_router)
setup_exception_handlers(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )
