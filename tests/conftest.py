import asyncio
from typing import AsyncGenerator, Generator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from source.config import TEST_DATABASE_ASYNC_URL, Base

async_engine = create_async_engine(
    TEST_DATABASE_ASYNC_URL, pool_size=10, echo=True, max_overflow=10
)

TestingAsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)


async def init_models() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_db_session(
    event_loop: asyncio.AbstractEventLoop,
) -> AsyncGenerator[AsyncSession, None]:
    await init_models()

    connection = await async_engine.connect()

    trans = await connection.begin()
    async_session = TestingAsyncSessionLocal(bind=connection)
    yield async_session

    await trans.rollback()
    await async_session.close()
    await connection.close()
