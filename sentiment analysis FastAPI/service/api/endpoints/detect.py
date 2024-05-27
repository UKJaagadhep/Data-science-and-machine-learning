from fastapi import APIRouter
from service.core.logic.inference_onnx import sentiment_analyzer
from service.core.schemas.input import APIInput
from service.core.schemas.output import APIOutput

sentiment_router = APIRouter()

@sentiment_router.post("/analyze", response_model = APIOutput)
async def sentiment(input : APIInput):
    return sentiment_analyzer(input.text)
