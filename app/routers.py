from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/")
def get_main_page():
    return dict(test='True')
