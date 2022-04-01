from fastapi import FastAPI, Depends
from dataclasses import dataclass
from typing import Optional
from app.config import Settings, get_settings, CustomSwagger, LoggingConfig, ORJSONResponse


app = FastAPI(default_response_class=ORJSONResponse)

log = LoggingConfig().get_logger()

@dataclass
class User:
    name: str
    age: int
    email: Optional[str] = None

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
    return user

# override the default swagger ui
app.openapi = CustomSwagger(app).custom_openapi
 