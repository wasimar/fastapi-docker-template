import uuid
from fastapi import FastAPI, Depends
from dataclasses import dataclass
from typing import Optional
from datetime import timedelta
from redis import Redis, RedisError
from app.config import Settings, get_settings, CustomSwagger, LoggingConfig, ORJSONResponse


app = FastAPI(default_response_class=ORJSONResponse)

log = LoggingConfig().get_logger()

@dataclass
class User:
    name: str
    role: str
    email: Optional[str] = None

    def __post_init__(self) -> None:
        self._id = uuid.uuid4().hex

def redis_session_db(user, min_validity) -> int:
    try:
        redis_client = Redis("redis", db=0, socket_timeout=2, socket_connect_timeout=2)
        id_check = redis_client.get(user.name)
        if id_check is None:
            redis_client.setex(user.name, value=user._id, time=timedelta(minutes=min_validity))
            return None
        return id_check
    except RedisError as e:
        log.error(f"Redis error: {e}")
        return None
    finally:
        redis_client.close()

@app.get("/")
async def base_response(settings: Settings = Depends(get_settings)):
    log.debug("Got settings: %s", settings)
    return {
        "message": "Hello World",
        "environment": settings.environment,
        "testing": settings.testing
    }
@app.post("/users")
async def create_user(user: User):
    log.debug("Got user: %s", user)
    r = redis_session_db(user=user, min_validity=5)
    if r is not None:
        log.debug( f"User {user.name} already exists with id {r}")
        user._id = r
    return user

# override the default swagger ui
app.openapi = CustomSwagger(app).custom_openapi
 