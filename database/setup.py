import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine_url = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/workflow_scratch_2"
)
engine = create_engine(engine_url)
AsyncEngine = create_async_engine(engine_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    async with AsyncSession(AsyncEngine) as session:
        try:
            yield session
        finally:
            await session.close()
