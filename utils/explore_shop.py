from playwright.sync_api import sync_playwright

from pages.shop_page import ShopPage
from utils.config import BASE_URL, AUTH_STATE_PATH
from utils.session_helper import restore_session_storage


def describe_price_click(context, label):
    page = context.new_page()
    shop_page = ShopPage(page)
    shop_page.open(BASE_URL)
    shop_page.accept_cookies()
    shop_page.select_first_item()
    page.wait_for_timeout(3000)

    print(f"--- {label} ---")
    dialogs = page.get_by_role("dialog")
    if dialogs.count():
        print(dialogs.first.aria_snapshot())
    else:
        print("No dialog found after the click")
    print("Payment iframes:", page.locator('iframe[title="Stumble Guys - Payment platform"]').count())
    page.close()


def explore_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        visitor = browser.new_context()
        describe_price_click(visitor, "Visitor, not logged in")
        visitor.close()

        member = browser.new_context(storage_state=AUTH_STATE_PATH)
        restore_session_storage(member)
        describe_price_click(member, "Logged in with saved session")
        member.close()

        browser.close()


if __name__ == "__main__":
    explore_shop()