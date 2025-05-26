"""
Asynchronous Kafka producer service using aiokafka for event publishing.

This module defines a KafkaProducerService class that manages the lifecycle
of an aiokafka AIOKafkaProducer, enabling asynchronous connection handling
and message sending to a specified Kafka topic. The Kafka broker URL and topic
are configurable via environment variables.

Constants:
- KAFKA_TOPIC: Kafka topic name for publishing events (default: "author-book-events").
- KAFKA_BROKER: Kafka broker address (default: "kafka:9092").

Classes:
- KafkaProducerService: Manages async Kafka producer connection and message sending.

Variables:
- kafka_producer: Singleton instance of KafkaProducerService for reuse.
"""

import os
import json
from typing import Optional
from aiokafka import AIOKafkaProducer

KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "author-book-events")
KAFKA_BROKER: str = os.getenv("KAFKA_BROKER", "kafka:9092")


class KafkaProducerService:
    """
    Asynchronous Kafka producer service to send JSON-encoded events.

    Handles starting and stopping of the Kafka producer connection,
    and provides a method to send events with a string key and JSON payload.

    Attributes:
        _producer (Optional[AIOKafkaProducer]): Internal Kafka producer instance.
    """

    def __init__(self) -> None:
        self._producer: Optional[AIOKafkaProducer] = None

    async def start(self) -> None:
        """
        Initialize and start the Kafka producer connection.
        """
        self._producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
        await self._producer.start()

    async def stop(self) -> None:
        """
        Stop and close the Kafka producer connection if active.
        """
        if self._producer:
            await self._producer.stop()

    async def send_event(self, key: str, payload: dict) -> None:
        """
        Send an event message to Kafka with a UTF-8 encoded key and JSON-encoded payload.

        Args:
            key (str): The message key used for partitioning.
            payload (dict): The JSON-serializable payload to send.

        Raises:
            RuntimeError: If the producer has not been started.
        """
        if not self._producer:
            raise RuntimeError("Kafka producer is not started.")
        await self._producer.send_and_wait(
            topic=KAFKA_TOPIC,
            key=key.encode("utf-8"),
            value=json.dumps(payload).encode("utf-8"),
        )


kafka_producer = KafkaProducerService()
