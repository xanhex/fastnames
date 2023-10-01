"""Database settings and services."""
from fastnames import config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = config.Settings().database_url

engine = create_async_engine(
    DATABASE_URL,
    # connect_args={'check_same_thread': False},
)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()


async def init_models() -> None:
    """Create all tables on app startup."""
    async with engine.begin() as conn:
        # To clear DB before re-creating it
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
