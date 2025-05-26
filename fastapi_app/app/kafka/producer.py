import os
import json
from aiokafka import AIOKafkaProducer

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "author-book-events")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")

class KafkaProducerService:
    def __init__(self):
        self._producer: AIOKafkaProducer | None = None

    async def start(self):
        self._producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
        await self._producer.start()

    async def stop(self):
        if self._producer:
            await self._producer.stop()

    async def send_event(self, key: str, payload: dict):
        if not self._producer:
            raise RuntimeError("Kafka producer is not started.")
        await self._producer.send_and_wait(
            topic=KAFKA_TOPIC,
            key=key.encode("utf-8"),
            value=json.dumps(payload).encode("utf-8")
        )

kafka_producer = KafkaProducerService()
