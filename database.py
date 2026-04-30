import aiosqlite
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv

import os

load_dotenv()

# two options db uls one for local usage and the other for production 
DATABASE_URL = os.getenv("DATABASE_URL", 'sqlite+aiosqlite:///spotify_users.db')

print(f"Using database: {DATABASE_URL}")

# check same threads = False is required for sqlite to allow multiple threads to access the database concurrently, which is necessary for asynchronous operations.
# the async engine is essentially what drives / starts the db operations
engine = create_async_engine(DATABASE_URL)

# this is what creates the db session
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

# this is the session fetcher which allows queries into the db
async def get_async_session():
  async with async_session_maker() as session:
    yield session



