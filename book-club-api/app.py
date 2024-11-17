from enum import Enum
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os
from .routers import users

load_dotenv()


app = FastAPI()


db = create_engine(os.environ.get('DATABASE_URL'))
SQLModel.metadata.create_all(db)


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
