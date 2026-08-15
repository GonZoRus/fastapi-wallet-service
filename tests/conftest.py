from uuid import UUID

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
from database import get_session
from main import app
from models import Base, Wallet

TEST_DB_NAME = "wallet_test_db"

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
)

test_engine = create_async_engine(TEST_DATABASE_URL)

test_async_session = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_test_session():
    async with test_async_session() as session:
        yield session


# Подменяем рабочую зависимость БД на тестовую
app.dependency_overrides[get_session] = get_test_session


# Подготовка структуры тестовой БД
@pytest_asyncio.fixture(scope="session", autouse=True, loop_scope="session")
async def prepare_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Подготовка данных для тестов
@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def test_wallet():
    wallet = Wallet()
    async with test_async_session() as session:
        wallet.wallet_uuid = UUID("550e8400-e29b-41d4-a716-446655440000")
        wallet.balance = 600
        session.add(wallet)
        await session.commit()

    yield wallet

    async with test_async_session() as session:
        wallet_from_db: Wallet | None = await session.get(Wallet, wallet.wallet_uuid)
        if wallet_from_db is not None:
            await session.delete(wallet_from_db)
            await session.commit()
