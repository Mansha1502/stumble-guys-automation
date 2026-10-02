from appium import webdriver
from appium.options.common import AppiumOptions

from utils.config import BASE_URL, BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY

HUB_URL = "https://hub.browserstack.com/wd/hub"


def build_options():
    options = AppiumOptions()
    options.set_capability("browserName", "chromium")
    options.set_capability("bstack:options", {
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
        "deviceName": "iPhone 15",
        "osVersion": "17",
        "realMobile": True,
        "projectName": "Stumble Guys automation",
        "buildName": "mobile smoke",
        "sessionName": "open home page",
    })
    return options


def run_smoke_test():
    if not BROWSERSTACK_USERNAME or not BROWSERSTACK_ACCESS_KEY:
        raise SystemExit("BrowserStack keys are missing from .env")

    driver = webdriver.Remote(HUB_URL, options=build_options())
    try:
        driver.get(BASE_URL)
        print("Opened:", driver.current_url)
        print("Title:", driver.title)
    finally:
        driver.quit()


if __name__ == "__main__":
    run_smoke_test()