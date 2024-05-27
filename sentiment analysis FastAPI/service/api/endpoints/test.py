from fastapi import APIRouter

test_router = APIRouter()

@test_router.get("/test")
async def tester():
    return {"testing" : "testing"}