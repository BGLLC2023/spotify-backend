from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from database import async_session_maker, engine
from models import Base
from analytics_router import router as analytics_router
from fastapi.middleware.cors import CORSMiddleware







# function for creating database tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# defines async contect manager and lifespan function
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


# app instance with lifespan function which creates db tables on start up 
app = FastAPI(lifespan=lifespan)

# dictates front url that can access the beackend and do database operations 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)

app.include_router(analytics_router)