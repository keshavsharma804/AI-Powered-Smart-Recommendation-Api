import redis

redis_client = redis.Redis(
    host="localhost",
    port=6385,
    db=0,
    decode_responses=False
)
