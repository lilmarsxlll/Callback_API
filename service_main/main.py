from contextlib import asynccontextmanager

import uvicorn


from src.config.logging_config import get_logger, setup_logging
from fastapi import FastAPI

from src.kafka_client import start_consumer, stop_consumer
from src.routes.routes import router

from src.db import db

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    await db.connect()
    await start_consumer()
    yield
    await stop_consumer()
    await db.disconnect()


app = FastAPI(lifespan=lifespan, title="Reservation API")
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
