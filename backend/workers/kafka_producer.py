"""Kafka producer helper for location ingestion."""

from __future__ import annotations

import json
from typing import Any

from kafka import KafkaProducer


class DriverLocationProducer:
    def __init__(self, bootstrap_servers: str | list[str], topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda value: json.dumps(value).encode('utf-8'),
            key_serializer=lambda value: str(value).encode('utf-8'),
            acks='all',
            retries=5,
            enable_idempotence=True,
        )

    def send(self, key: str, payload: dict[str, Any]) -> None:
        self._producer.send(self.topic, key=key, value=payload)

    def flush(self) -> None:
        self._producer.flush()
