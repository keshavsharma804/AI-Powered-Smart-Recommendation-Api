# app/rate_limit.py

import time
from .redis_client import redis_client

def check_rate_limit(key: str, limit: int = 30, window_sec: int = 60):
    """
    Returns True if allowed, False if rate-limited.
    Example: 30 requests per minute per key.
    """

    redis_key = f"rate:{key}"

    pipe = redis_client.pipeline()

    pipe.incr(redis_key)
    pipe.expire(redis_key, window_sec)

    req_count, _ = pipe.execute()

    return req_count <= limit
