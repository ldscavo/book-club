from enum import Enum
from fastapi import FastAPI
from dotenv import load_dotenv
from database import create_tables
from routers import users

load_dotenv()

create_tables()

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World!"}

app.include_router(users.router)


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
