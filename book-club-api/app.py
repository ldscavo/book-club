from fastapi import FastAPI
from database import create_tables
from routers import users, auth

create_tables()

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
