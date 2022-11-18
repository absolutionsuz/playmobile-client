import httpx
import pytest

from playmobile.client import HttpClient
from playmobile.entities import Credentials
from playmobile.test_utils import generate_string


@pytest.fixture()
def base_url() -> httpx.URL:
    return httpx.URL("https://example.com/")


@pytest.fixture()
def account() -> Credentials:
    return Credentials(
        username=generate_string(),
        password=generate_string(),
    )


@pytest.fixture()
def client(base_url: httpx.URL, account: Credentials) -> HttpClient:
    return HttpClient(
        account=account,
        base_url=base_url,
        session=httpx.Client(),
    )
