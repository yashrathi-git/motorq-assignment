import os
from pydantic import RedisDsn
import redis

redis_client = redis.Redis(
    host=os.getenv('REDIS_URL'),
    port=int(os.getenv('REDIS_PORT')),
    db=int(os.getenv('REDIS_DB')),
    password=os.getenv('REDIS_PASSWORD')
)