from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self):
        return self.page.title()

    def accept_cookies(self):
        accept_button = self.page.get_by_role("button", name="Accept All")
        try:
            accept_button.click(timeout=5000)
        except PlaywrightTimeout:
            pass