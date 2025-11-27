from fastapi import APIRouter
from app.core.redis_driver import RedisDriver

router = APIRouter(prefix="/stream", tags=["stream"])

@router.get("/")
def get_stream(count: int = 10):
    redis = RedisDriver()
    streams = redis.read_stream('threat_stream', count)
    return {"streams": streams}