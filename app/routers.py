from fastapi import APIRouter

from app.currencies.routers import router as currency_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(currency_router)
