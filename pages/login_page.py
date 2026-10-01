from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    def enter_email(self, email: str):
        self.page.get_by_label("Email").fill(email)

    def click_continue(self):
        self.page.get_by_role("button", name="Continue").click()