import uvicorn
from fastapi import FastAPI

from app.config.settings import settings
from app.routers import api_router


app = FastAPI(
    title=settings.app.title,
    debug=settings.app.debug,
)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )
