from fastapi import FastAPI
from database import create_tables
import auth.routes as auth_routes
import users.routes as user_routes
import clubs.routes as club_routes

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(club_routes.router)
