
import time  
from redis import Redis, TimeoutError
from dataclasses import dataclass
import fakeredis
import uuid

from src.app.main import redis_session_db

@dataclass
class User:
    name: str
    role: str
    def __post_init__(self) -> None:
        self._id = uuid.uuid4().hex

def test_redis_session_validity():
    """
    Test that the redis_session_db function returns the correct value.
    """
    redis_client = fakeredis.FakeStrictRedis()
    user = User(name="test", role="test")
    
    min_val = 0.1
    temp_id = redis_session_db(redis_client,user=user, min_validity=min_val)
    assert temp_id is None
    temp_id = redis_session_db(redis_client,user=user, min_validity=min_val)
    assert temp_id is not None # got back same id assigned to user
    time.sleep(min_val*60) 
    temp_id = redis_session_db(redis_client,user=user, min_validity=min_val)
    assert temp_id is None # id expired
