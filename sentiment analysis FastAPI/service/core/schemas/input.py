from pydantic import BaseModel

class APIInput(BaseModel):
    text : str
