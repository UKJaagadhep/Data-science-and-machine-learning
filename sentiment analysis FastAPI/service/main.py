from fastapi import FastAPI
from service.api.api import main_router
import onnxruntime as rt

app = FastAPI(project_name = "Sentiment Analysis")
app.include_router(main_router)

providers = ['CPUExecutionProvider']
m = rt.InferenceSession("service/xtremedistill_quantized.onnx", providers = providers)



@app.get("/")
async def root():
    return {"hello" : "world"}