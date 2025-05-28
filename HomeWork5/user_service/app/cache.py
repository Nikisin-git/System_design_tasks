import redis.asyncio as redis

redis_client = redis.from_url("redis://cache:6379", decode_responses=True)