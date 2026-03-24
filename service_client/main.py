import asyncio
import uuid

import httpx

from src.config.logger_config import setup_logging, get_logger
from src.config.settings_for_client import settings
from src.kafka_client import send_reservation, start_producer, stop_producer

setup_logging()
logger = get_logger(__name__)

JWT_TOKEN: str | None = None


async def get_jwt_token():
    global JWT_TOKEN
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.RESERVATION_API_URL}/login",
                json={
                    "username": settings.SERVICE_CLIENT_USERNAME,
                    "password": settings.SERVICE_CLIENT_PASSWORD,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            JWT_TOKEN = data.get("access_token")
            logger.info("JWT token successfully gotten from service_main")
        except Exception as e:
            logger.error(f"Error getting JWT token: {e}")
            raise


async def make_reservation():

    await asyncio.sleep(5)
    await start_producer()
    await get_jwt_token()
    try:
        while True:
            reservation_id = str(uuid.uuid4())
            reservation = {
                "reservation_id": reservation_id,
                "product_id": "12345",
                "quantity": 1,
            }

            try:
                await send_reservation(reservation)
                logger.info(f"[{reservation_id}] Reservation sent to Kafka")
            except Exception as e:
                logger.error(f"[{reservation_id}] Error sending reservation: {e}")

            await asyncio.sleep(3)
    finally:
        await stop_producer()


if __name__ == "__main__":
    asyncio.run(make_reservation())
