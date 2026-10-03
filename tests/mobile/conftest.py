from pathlib import Path

import pytest
from appium import webdriver

from utils.browserstack import HUB_URL, build_options
from utils.config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, TEST_EMAIL


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, f"rep_{outcome.get_result().when}", outcome.get_result())


def require_browserstack_keys():
    if not (BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY):
        pytest.skip("BrowserStack keys are missing from .env")


def finish_session(driver, request):
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        Path("test-results").mkdir(exist_ok=True)
        driver.save_screenshot(f"test-results/{request.node.name}.png")
    driver.quit()


@pytest.fixture
def mobile_driver(request):
    require_browserstack_keys()

    driver = webdriver.Remote(HUB_URL, options=build_options(request.node.name))
    yield driver
    finish_session(driver, request)


@pytest.fixture
def interactive_mobile_driver(request):
    require_browserstack_keys()
    if not TEST_EMAIL:
        pytest.skip("TEST_EMAIL is not set in .env")
    if request.config.getoption("capture") != "no":
        pytest.skip("This test asks for a login code, run it with -s")

    # Long idle timeout, because typing the code from the inbox takes a while
    options = build_options(request.node.name, idle_timeout=300)
    driver = webdriver.Remote(HUB_URL, options=options)
    yield driver
    finish_session(driver, request)