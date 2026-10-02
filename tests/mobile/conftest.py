import pytest
from appium import webdriver

from utils.browserstack import HUB_URL, build_options
from utils.config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY


@pytest.fixture
def mobile_driver(request):
    if not (BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY):
        pytest.skip("BrowserStack keys are missing from .env")

    driver = webdriver.Remote(HUB_URL, options=build_options(request.node.name))
    yield driver
    driver.quit()