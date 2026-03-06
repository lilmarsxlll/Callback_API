from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


from config.settings import settings


class Database:
    def __init__(self) -> None:
        self.engine = None
        self.session: async_sessionmaker[AsyncSession] | None = None

    async def connect(self) -> None:
        self.engine = create_async_engine(settings.get_db_url())
        self.session = async_sessionmaker(bind=self.engine)

    async def disconnect(self) -> None:
        if self.session:
            await self.engine.dispose()

    async def get_session(self) -> AsyncGenerator[async_sessionmaker[AsyncSession], Any]:
        async_session_maker = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session_maker() as session:
            yield session


db = Database()
