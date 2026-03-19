import asyncio
import json

from aiokafka import AIOKafkaConsumer


from src.config.logging_config import get_logger
from src.config.settings_for_main import settings

from src.db import db
from src.models import Product, Reservation

consumer: AIOKafkaConsumer | None = None
consumer_task: asyncio.Task | None = None

KAFKA_BOOTSTRAP_SERVER = settings.KAFKA_BOOTSTRAP_SERVER
KAFKA_TOPIC = settings.KAFKA_TOPIC
KAFKA_GROUP_ID = settings.KAFKA_GROUP_ID

logger = get_logger(__name__)


async def start_consumer():
    global consumer, consumer_task
    logger.info("Starting consumer")
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
        group_id=KAFKA_GROUP_ID,
        auto_offset_reset="earliest",
    )
    await asyncio.sleep(2)
    await consumer.start()
    logger.info("Consumer connected to Kafka")
    consumer_task = asyncio.create_task(_consume_loop())
    logger.info("Consumer started")


async def stop_consumer():
    global consumer, consumer_task
    if consumer_task:
        consumer_task.cancel()
        await consumer_task
    if consumer:
        await consumer.stop()
        logger.info("Consumer stopped")


async def _consume_loop():
    logger.info("Consume loop started")
    global consumer, consumer_task
    async for msg in consumer:
        logger.info("Message received")
        data = json.loads(msg.value.decode())
        logger.info(f"Consumer received: {data}")
        await handle_reservation(data)


async def handle_reservation(data: dict):
    async with db.session() as session:
        async with session.begin():
            product = await session.get(Product, data["product_id"])
            if not product:
                logger.info("Product not found")
                return
            if product.available_quantity < data["quantity"]:
                logger.info("Not enough stock")
                return

            existing = await session.get(Reservation, data["reservation_id"])
            if existing:
                logger.info(f"Reservation {data['reservation_id']} already exists")
                return

            product.available_quantity -= data["quantity"]
            reservation = Reservation(
                reservation_id=data["reservation_id"],
                product_id=data["product_id"],
                required_quantity=data["quantity"],
            )
            session.add(reservation)
            await session.flush()
