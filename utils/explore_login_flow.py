from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

from utils.config import BASE_URL, TEST_EMAIL


def describe(page, label):
    # Prints where the browser is and what it shows, never what is typed in the fields
    url = urlsplit(page.url)
    print(f"--- {label}: {url.netloc}{url.path}")
    for box in page.locator("input:visible").all():
        print(f"  input type={box.get_attribute('type')} maxlength={box.get_attribute('maxlength')} "
              f"typed_chars={len(box.input_value())}")
    for button in page.locator("button:visible").all():
        text = button.inner_text().strip()
        if text:
            print(f"  button {text!r}")


def explore_login_flow():
    Path("test-results").mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False)
        context = browser.new_context(**p.devices["iPhone 15"])
        page = context.new_page()
        page.goto(BASE_URL)
        page.get_by_role("button", name="Accept All").click()
        page.get_by_role("button", name="avatar").click()
        page.get_by_role("button", name="Login").click()
        page.get_by_role("button", name="Email logo").click()
        page.locator('[data-test-id="Input"]').fill(TEST_EMAIL)
        page.locator('[data-test-id="site-email-input-submit-button"]').click()
        page.wait_for_timeout(6000)
        describe(page, "after submitting the email")
        page.screenshot(path="test-results/login_flow_1.png")

        continue_button = page.get_by_role("button", name="Continue", exact=True)
        if continue_button.count() and continue_button.first.is_visible():
            continue_button.first.click()
            page.wait_for_timeout(6000)
            describe(page, "after tapping Continue")
            page.screenshot(path="test-results/login_flow_2.png")

        input("Look at the browser, then press Enter here to close it... ")
        browser.close()


if __name__ == "__main__":
    explore_login_flow()