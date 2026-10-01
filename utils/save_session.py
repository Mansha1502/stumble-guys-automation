from pathlib import Path

from playwright.sync_api import sync_playwright

from utils.config import BASE_URL, AUTH_STATE_PATH
from utils.session_helper import save_session_storage


def save_login_session():
    Path(AUTH_STATE_PATH).parent.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE_URL)

        print("Log in with your email and the OTP in the browser window.")
        print("Wait until the header shows you as logged in, and check")
        print("that the avatar menu no longer offers Login.")
        input("Then press Enter here to save the session... ")

        context.storage_state(path=AUTH_STATE_PATH, indexed_db=True)
        keys = save_session_storage(page)
        print("sessionStorage keys saved:", len(keys), keys)
        browser.close()


if __name__ == "__main__":
    save_login_session()