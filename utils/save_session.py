from pathlib import Path

from playwright.sync_api import sync_playwright

from utils.config import BASE_URL, AUTH_STATE_PATH


def save_login_session():
    Path(AUTH_STATE_PATH).parent.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE_URL)

        print("Log in with your email and the OTP in the browser window.")
        input("Once you are logged in, press Enter here to save the session... ")

        context.storage_state(path=AUTH_STATE_PATH, indexed_db=True)
        browser.close()


if __name__ == "__main__":
    save_login_session()