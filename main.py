from contextlib import asynccontextmanager


import uvicorn
from fastapi import FastAPI

from app.models import Base
from app.routes import router
from app.db import db


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    await db.connect()
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app)


