"""Kafka consumer placeholder for location processing."""

from __future__ import annotations

from typing import Any


class LocationConsumer:
    def __init__(self, bootstrap_servers: str | list[str], group_id: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topic = topic

    def process_message(self, message: Any) -> dict[str, Any]:
        return {'status': 'received', 'offset': getattr(message, 'offset', None)}
