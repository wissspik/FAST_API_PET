import os

from redis.asyncio import Redis


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

redis_client: Redis = Redis.from_url(REDIS_URL, decode_responses=True)
