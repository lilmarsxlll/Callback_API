import asyncio
import json

from aiokafka import AIOKafkaProducer

from src.config.logger_config import get_logger
from src.config.settings_for_client import settings

producer: AIOKafkaProducer | None = None
KAFKA_BOOTSTRAP_SERVER = settings.KAFKA_BOOTSTRAP_SERVER
KAFKA_TOPIC = settings.KAFKA_TOPIC

logger = get_logger(__name__)


async def start_producer() -> None:
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER)
    await asyncio.sleep(4)
    await producer.start()
    logger.info("Producer started")


async def stop_producer() -> None:
    global producer
    await producer.stop()
    logger.info("Producer stopped")


async def send_reservation(reservation_data: dict) -> None:
    global producer
    if not producer:
        raise RuntimeError("Producer not started")
    await producer.send_and_wait(KAFKA_TOPIC, json.dumps(reservation_data).encode())
