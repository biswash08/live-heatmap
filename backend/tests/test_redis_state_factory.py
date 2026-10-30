from infrastructure.redis.state_store import RedisStateStore, get_state_store


def test_redis_state_store_factory_uses_redis_when_enabled(monkeypatch):
    class FakeRedisClient:
        def ping(self):
            return True

        def hset(self, *args, **kwargs):
            return 1

        def sadd(self, *args, **kwargs):
            return 1

    class FakeRedisModule:
        @staticmethod
        def from_url(url, decode_responses=True):
            assert url
            return FakeRedisClient()

    FakeRedisModule.Redis = FakeRedisModule

    monkeypatch.setenv('USE_REDIS_STATE', 'true')
    monkeypatch.setenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
    import infrastructure.redis.state_store as state_store_module

    monkeypatch.setattr(state_store_module, 'redis', FakeRedisModule())
    store = get_state_store()

    assert isinstance(store, RedisStateStore)
    assert store._redis_ready is True
