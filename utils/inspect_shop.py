import sys

from playwright.sync_api import sync_playwright

from utils.config import BASE_URL, AUTH_STATE_PATH
from utils.session_helper import restore_session_storage


def inspect_page(path: str = "/shop"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=AUTH_STATE_PATH)
        restore_session_storage(context)
        page = context.new_page()
        page.goto(BASE_URL.rstrip("/") + path)
        page.pause()
        browser.close()


if __name__ == "__main__":
    inspect_page(sys.argv[1] if len(sys.argv) > 1 else "/shop")