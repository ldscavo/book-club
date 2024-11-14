from typing import Union
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

class ModelName(str, Enum):
    foo = "foo"
    bar = "bar"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.foo:
        return {"name": model_name, "value": "fighters"}
    if model_name is ModelName.bar:
        return {"name": model_name, "value": "none"}

    return {}