import pytest
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@pytest.fixture(name="json_response")
def json_response(function_scoped_container_getter) -> str:
    """
    Waits for the app to come online, then returns the URL to access the
    homepage.
    """
    service = function_scoped_container_getter.get('web').network_info[0]

    base_url = f"http://{service.hostname}:{service.host_port}"

    retry = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504],
    )

    session = Session()
    session.mount('http://', HTTPAdapter(max_retries=retry))

    assert session.get(f'{base_url}/').json()['message'] == 'Hello World'

    return base_url