from pathlib import Path

from playwright.sync_api import sync_playwright

from utils.config import BASE_URL, AUTH_STATE_PATH
from utils.session_helper import restore_session_storage


def check_session():
    Path("test-results").mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=AUTH_STATE_PATH)
        restore_session_storage(context)
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_timeout(4000)

        accept = page.get_by_role("button", name="Accept All")
        if accept.count():
            accept.click()
            page.wait_for_timeout(1500)

        login_visible = page.get_by_role("button", name="Login").first.is_visible()
        print("Login button visible:", login_visible)
        print("Buttons with 'avatar' in the name:", page.get_by_role("button", name="avatar").count())

        page.screenshot(path="test-results/session_check.png")
        page.wait_for_timeout(3000)
        browser.close()


if __name__ == "__main__":
    check_session()