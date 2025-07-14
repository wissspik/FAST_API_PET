import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

from aiokafka import AIOKafkaConsumer
from dotenv import load_dotenv
from fastapi import FastAPI

from profile_service.database.base import SessionDep
from profile_service.utils.sql_request import (create_user_id,
                                               get_user_id_profile,)


load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP")
LOGS_TOPIC = os.getenv("LOGS_TOPIC")
GROUP_ID = os.getenv("GROUP_ID")

logger = logging.getLogger("kafka-consumer")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
logger.addHandler(handler)


async def consume_loop(consumer: AIOKafkaConsumer):
    """ """
    async for msg in consumer:
        try:
            payload = json.loads(msg.value.decode("utf-8"))
            if not await get_user_id_profile(payload["user_id"]):
                created_profile = await create_user_id(
                    payload["user_id"], payload["login"]
                )
                logger.info(f"Created profile: {created_profile.id}")
            logger.info(f"Consumed message_service: {payload}")
        except json.JSONDecodeError:
            logger.error("Failed to decode message_service", exc_info=True)

        except Exception:
            logger.exception("Error in consume_loop")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup: инициализируем и запускаем консьюмера + фоновую задачу ---
    consumer = AIOKafkaConsumer(
        LOGS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",  # с какого места читать при первом старте
        enable_auto_commit=True,  # будем автоматически коммитить смещения
    )
    await consumer.start()
    app.state.consumer = consumer
    app.state.consumer_task = asyncio.create_task(consume_loop(consumer))

    yield  # здесь FastAPI запускает сервер

    # --- Shutdown: отменяем задачу и останавливаем консьюмера ---
    app.state.consumer_task.cancel()
    try:
        await app.state.consumer_task
    except asyncio.CancelledError:
        pass
    await consumer.stop()
