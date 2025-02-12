from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.REDIS_HOST != "" or settings.REDIS_PORT != "":
        redis = aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
        )
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        yield
    yield
