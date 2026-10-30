"""Kafka consumer for processing driver location events."""

from __future__ import annotations

import json
from typing import Any

from infrastructure.redis.state_store import DriverStateStore
from workers.location_processor import process_location_event


class LocationConsumer:
    def __init__(
        self,
        bootstrap_servers: str | list[str],
        group_id: str,
        topic: str,
        state_store: DriverStateStore | None = None,
    ):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topic = topic
        self.store = state_store or DriverStateStore.shared()

    def process_message(self, message: Any) -> dict[str, Any]:
        payload = message
        offset = getattr(message, 'offset', None)

        if hasattr(message, 'value'):
            payload = message.value

        if isinstance(payload, (bytes, bytearray)):
            payload = payload.decode('utf-8')

        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                return {'status': 'rejected', 'offset': offset, 'reason': 'invalid_json'}

        if not isinstance(payload, dict):
            return {'status': 'rejected', 'offset': offset, 'reason': 'invalid_payload'}

        try:
            result = process_location_event(payload, self.store)
        except (TypeError, ValueError, KeyError):
            return {'status': 'rejected', 'offset': offset, 'reason': 'invalid_event', 'payload': payload}

        return {
            'status': 'processed',
            'offset': offset,
            'event_id': payload.get('event_id'),
            'driver_id': payload.get('driver_id'),
            'result': result,
        }
