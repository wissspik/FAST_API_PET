import os
from datetime import datetime
import asyncio
from fastapi import FastAPI
import json
import logging
from aiokafka import AIOKafkaProducer
from dotenv import load_dotenv

from contextlib import asynccontextmanager

load_dotenv()

KAFKA_BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP')
LOGS_TOPIC = os.getenv('LOGS_TOPIC')

logger = logging.getLogger("kafka-producer") # создаем логгер kafka-logger
logger.setLevel(logging.INFO)


class KafkaLogHandler(logging.Handler):
    def __init__(self, producer: AIOKafkaProducer, topic: str):
        super().__init__()
        self.producer = producer
        self.topic = topic
    def emit(self, record):
        # cоздаю лог
        log_entry = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z", # время
            "level": record.levelname, # важность лога
            "message": record.getMessage(), # сообщение в логе
            "module": record.module, # имя модуля откуда будет идти log
            "funcName": record.funcName, # место, где лог бы создан
            "lineNo": record.lineno, # номер строки с вызовом
        }

        if hasattr(record, "user_id"):
            log_entry["user_id"] = record.user_id
        if hasattr(record, "login"):
            log_entry["login"] = record.login
        payload = json.dumps(log_entry).encode("utf-8")
        asyncio.get_event_loop().create_task(
            self.producer.send_and_wait(self.topic, payload)
    )


@asynccontextmanager
async def lifespan(app : FastAPI):
    # --- Startup ---
    app.state.kafka_producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        acks="all",
        retry_backoff_ms=100,  # пауза между автоматическими переподключениями
        request_timeout_ms=20000,  # сколько ждать ответа от брокера
    )
    await app.state.kafka_producer.start()
    kafka_handler = KafkaLogHandler(app.state.kafka_producer, LOGS_TOPIC)
    logger.addHandler(kafka_handler)
    logger.info("Kafka producer started")

    yield

    # --- Shutdown ---
    logger.info(f"Kafka producer stopped.")
    await app.state.kafka_producer.stop()



