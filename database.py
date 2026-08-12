from sqlalchemy.ext.asyncio import (
	AsyncSession, create_async_engine,
	async_sessionmaker
)
from config import (
	DB_HOST, DB_PORT,
	DB_USER, DB_PASSWORD,
	DB_NAME
)

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)


async_session = async_sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False
)


async def get_session():
	async with async_session() as session:
		yield session
