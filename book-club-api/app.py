from fastapi import FastAPI
from database import create_tables
from routers import users, auth, clubs


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(clubs.router)
