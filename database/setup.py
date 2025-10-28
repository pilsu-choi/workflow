import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel

from setting.logger import get_logger

logger = get_logger(__name__)

async_engine_url = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/workflow_scratch_2",
)
AsyncEngine = create_async_engine(async_engine_url)


async def get_async_db() -> AsyncSession:
    async with AsyncSession(AsyncEngine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database connection failed: {e}", exc_info=True)
            raise e
        finally:
            await session.close()


async def validate():
    from pydantic_core import ValidationError

    # db connection validation
    try:
        from sqlalchemy.ext.asyncio import create_async_engine

        engine = create_async_engine(async_engine_url)
        async with engine.connect() as conn:
            await conn.close()
    except Exception as e:
        logger.error(f"Database validation failed: {e}", exc_info=True)
        raise ValidationError(f"Database validation failed: {e}")

    return True


async def create_tables():
    async with AsyncEngine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("✅ Tables created successfully")
