from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

from pages.shop_page import ShopPage
from utils.config import BASE_URL, AUTH_STATE_PATH
from utils.session_helper import restore_session_storage

CHECKOUT_HOSTS = ("xsolla", "stripe")


def short(url):
    parts = urlsplit(url)
    return f"{parts.netloc}{parts.path}"


def debug_payment_frames():
    Path("test-results").mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=AUTH_STATE_PATH)
        restore_session_storage(context)
        page = context.new_page()

        shop_page = ShopPage(page)
        shop_page.open(BASE_URL)
        shop_page.accept_cookies()
        shop_page.open_first_item()
        shop_page.continue_to_card_details()
        page.wait_for_timeout(15000)

        for frame in page.frames:
            if not any(host in frame.url for host in CHECKOUT_HOSTS):
                continue
            print("---", short(frame.url))
            try:
                print(frame.locator("body").aria_snapshot(timeout=3000))
            except Exception as error:
                print("could not read this frame:", type(error).__name__)

        page.screenshot(path="test-results/purchase_debug.png")
        browser.close()


if __name__ == "__main__":
    debug_payment_frames()