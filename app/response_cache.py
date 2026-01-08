

import hashlib
import json
import pickle
from .redis_client import redis_client

def make_response_cache_key(query: str, products):
    payload = {
        "query": query,
        "products": [p.dict() for p in products]
    }

    raw = json.dumps(payload, sort_keys=True)
    return "resp:" + hashlib.sha256(raw.encode()).hexdigest()


def get_cached_response(key: str):
    cached = redis_client.get(key)
    if cached:
        return pickle.loads(cached)
    return None


def store_response(key: str, response, ttl=300):
    redis_client.setex(key, ttl, pickle.dumps(response))
