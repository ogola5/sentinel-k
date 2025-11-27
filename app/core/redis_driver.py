import redis
import ssl
from app.core.config import settings

class RedisDriver:
    def __init__(self):
        ssl_flag = settings.redis_use_ssl

        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            username=settings.redis_user,
            password=settings.redis_password,
            ssl=ssl_flag,
            ssl_cert_reqs=ssl.CERT_NONE if ssl_flag else None,  # only required if SSL
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )

    def add_to_stream(self, stream_name: str, data: dict):
        try:
            self.client.xadd(stream_name, data)
        except redis.RedisError as e:
            print(f"Redis stream error (non-fatal): {e}")

    def read_stream(self, stream_name: str, count: int = 10):
        try:
            return self.client.xrevrange(stream_name, count=count)
        except redis.RedisError as e:
            print(f"Redis read error: {e}")
            return []

# Singleton instance
redis_driver = RedisDriver()
