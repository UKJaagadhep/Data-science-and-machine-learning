from fastapi import APIRouter
from service.api.endpoints.detect import sentiment_router
from service.api.endpoints.test import test_router

main_router = APIRouter()

main_router.include_router(test_router)
main_router.include_router(sentiment_router)