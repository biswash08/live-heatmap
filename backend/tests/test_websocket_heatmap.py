import asyncio
import json

from channels.testing import WebsocketCommunicator

from config.asgi import application


def test_heatmap_websocket_connects_and_heartbeat():
    async def run_test():
        communicator = WebsocketCommunicator(application, '/ws/v1/heatmap/ktm/')
        connected, _ = await communicator.connect()
        assert connected is True

        first_message = json.loads(await communicator.receive_from())
        assert first_message['type'] in {'subscribed', 'heartbeat'}

        await communicator.send_to(json.dumps({'type': 'ping'}))
        pong = json.loads(await communicator.receive_from())
        assert pong['type'] == 'pong'

        await communicator.disconnect()

    asyncio.run(run_test())
