from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from infrastructure.redis.state_store import DriverStateStore


class HeatmapConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.city_id = self.scope['url_route']['kwargs'].get('city_id', 'ktm')
        self.group_name = f'heatmap_{self.city_id}'.replace('-', '_')

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.send_json({
            'type': 'subscribed',
            'city_id': self.city_id,
            'status': 'connected',
            'message': f'Connected to {self.city_id} heatmap updates',
        })

        self.heartbeat_task = asyncio.create_task(self.send_heartbeat())

    async def disconnect(self, close_code):
        if hasattr(self, 'heartbeat_task'):
            self.heartbeat_task.cancel()
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_heartbeat(self):
        try:
            while True:
                await asyncio.sleep(10)
                await self.send_json({
                    'type': 'heartbeat',
                    'city_id': self.city_id,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                })
        except asyncio.CancelledError:
            pass

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'ping':
            await self.send_json({
                'type': 'pong',
                'city_id': self.city_id,
                'timestamp': datetime.now(timezone.utc).isoformat(),
            })
            return

        if message_type == 'viewport':
            payload = {
                'type': 'viewport_update',
                'city_id': self.city_id,
                'viewport': content.get('viewport', {}),
                'cells': self._get_cell_snapshot(),
            }
            await self.send_json(payload)

    @database_sync_to_async
    def _get_cell_snapshot(self):
        store = DriverStateStore.shared()
        cells = []
        for driver_id, state in store.driver_states.items():
            if state.city_id != self.city_id:
                continue
            cells.append({
                'driver_id': driver_id,
                'h3_index': state.current_h3_cell,
                'driver_count': store.cell_counts.get(f'cell:{self.city_id}:{state.current_h3_cell}', 0),
            })
        return cells
