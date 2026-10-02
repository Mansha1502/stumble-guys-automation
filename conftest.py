import os

import pytest

from utils.config import BASE_URL, AUTH_STATE_PATH
from utils.session_helper import restore_session_storage


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def logged_in_page(browser, browser_context_args):
    if not os.path.exists(AUTH_STATE_PATH):
        pytest.skip("No saved session found. Run: python -m utils.save_session")

    context = browser.new_context(**browser_context_args, storage_state=AUTH_STATE_PATH)
    restore_session_storage(context)
    page = context.new_page()
    yield page
    context.close()