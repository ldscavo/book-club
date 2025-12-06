from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables
import auth.routes as auth_routes
import users.routes as user_routes
import clubs.routes as club_routes
import invitations.routes as invitation_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(club_routes.router)
app.include_router(invitation_routes.club_router)
app.include_router(invitation_routes.user_router)
