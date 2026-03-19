import asyncio
import uuid


from src.config.logger_config import setup_logging, get_logger
from src.kafka_client import send_reservation, start_producer, stop_producer

setup_logging()
logger = get_logger(__name__)


async def make_reservation():
    await start_producer()
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
