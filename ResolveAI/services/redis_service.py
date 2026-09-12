import json

import redis


class RedisService:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
    ):
        # This creates the connection/client object.
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        #This is simply a health/connectivity test.
    def ping(self) -> bool:
        return self.client.ping()

    def set_value(
        self,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ):
        self.client.set(key, value)

        if ttl_seconds is not None:
            self.client.expire(key, ttl_seconds)

    def get_value(self, key: str):
        return self.client.get(key)

    def set_json(
        self,
        key: str,
        value,
        ttl_seconds: int | None = None,
    ):
        if hasattr(value, "model_dump"):
            value = value.model_dump()

        self.client.set(
            key,
            json.dumps(value),
        )

        if ttl_seconds is not None:
            self.client.expire(key, ttl_seconds)

    def get_json(self, key: str):
        value = self.client.get(key)

        if value is None:
            return None

        return json.loads(value)