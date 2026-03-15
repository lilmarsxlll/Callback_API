import asyncio
import random

import httpx

from src.config.settings import settings
from src.config.logger_config import setup_logging, get_logger

RESERVATION_API_URL = settings.RESERVATION_API_URL
ACCESS_TOKEN = settings.ACCESS_TOKEN

setup_logging()
logger = get_logger(__name__)


async def make_reservation():
    while True:
        reservation_id = str(random.randint(1, 9999))
        payload = {
            "reservation_id": reservation_id,
            "product_id": "12345",
            "quantity": 1,
        }
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    RESERVATION_API_URL, json=payload, headers=headers
                )
                logger.info(
                    f"[{reservation_id}] Status: {response.status_code}, Response: {response.json()}"
                )
            except Exception as e:
                print(f"[{reservation_id}] Error: {e}")

        await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(make_reservation())
