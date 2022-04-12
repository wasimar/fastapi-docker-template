import json
from requests import post


pytest_plugins = ["docker_compose"]


def test_one_user_gets_unique_id(json_response: str):
    payload = json.dumps({
                        "name": "test",
                        "role": "dev"
                        })
    api = f"{json_response}/users"
    uid = post(api, data=payload).json()
    print(uid)
    assert len(uid) == 32

    # Send another request, to check if id changed.
    assert post(api, data=payload).json() == uid
