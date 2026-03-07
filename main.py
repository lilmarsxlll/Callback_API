from contextlib import asynccontextmanager


import uvicorn
from fastapi import FastAPI

from app.routes import router
from app.db import db


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app)
