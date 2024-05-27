from pydantic import BaseModel

class APIOutput(BaseModel):
    emotion : str