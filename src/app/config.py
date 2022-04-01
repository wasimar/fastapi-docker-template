
import os
from functools import lru_cache
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from pydantic import BaseSettings
import typing,orjson


import logging
import logging.config

class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev") # dev, test, prod
    testing: bool = os.getenv("TESTING", 0) # 0, 1

@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()

class ORJSONResponse(JSONResponse):
    media_type = "application/json"
    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(content)


class CustomSwagger(object):
    def __init__(self, app):
        self.app = app

    def custom_openapi(self):
        if self.app.openapi_schema:
            return self.app.openapi_schema
        openapi_schema = get_openapi(
            title="FastAPI Documention - OpenAPI 3.0",
            version="1.0.1",
            description="This is a very custom OpenAPI schema",
            routes=self.app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://bluanalytics.io/wp-content/uploads/2020/12/icon-300x300.png"
        }
        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema


class LoggingConfig():
    def __init__(self):
        self.level: str = os.getenv("LOG_LEVEL", "INFO") 
        self.logger: str = logging.getLogger(__name__)
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,  # this fixes the problem
            'handlers': {
                'default': {
                    'level':self.level,
                    'class':'logging.StreamHandler',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['default'],
                    'level': self.level,
                    'propagate': True
                }
            }
        })
        self.logger.info("Logging configured")
    
    def get_logger(self):
        return self.logger