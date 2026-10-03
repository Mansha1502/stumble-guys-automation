from appium.options.common import AppiumOptions

from utils.config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY

HUB_URL = "https://hub.browserstack.com/wd/hub"
DEVICE_NAME = "iPhone 15"
OS_VERSION = "17"


def build_options(session_name: str, idle_timeout: int | None = None) -> AppiumOptions:
    bstack_options = {
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
        "deviceName": DEVICE_NAME,
        "osVersion": OS_VERSION,
        "realMobile": True,
        "projectName": "Stumble Guys automation",
        "buildName": "mobile tests",
        "sessionName": session_name,
    }
    if idle_timeout:
        bstack_options["idleTimeout"] = idle_timeout

    options = AppiumOptions()
    # BrowserStack automates Chromium on iOS, since Chrome itself is not supported there
    options.set_capability("browserName", "chromium")
    options.set_capability("bstack:options", bstack_options)
    return options