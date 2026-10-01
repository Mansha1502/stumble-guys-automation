import pytest

from utils.config import BASE_URL


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL