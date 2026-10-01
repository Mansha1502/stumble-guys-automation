from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.avatar_button = page.get_by_role("button", name="avatar")
        self.login_button = page.get_by_role("button", name="Login")
        self.email_option = page.get_by_role("button", name="Continue with email")
        self.email_input = page.locator('[data-test-id="Input"]')
        self.submit_button = page.locator('[data-test-id="site-email-input-submit-button"]')
        self.otp_inputs = page.get_by_role("textbox")

    def open_login_options(self):
        self.avatar_button.click()
        self.login_button.click()

    def choose_email_login(self):
        self.email_option.click()

    def submit_email(self, email: str):
        self.email_input.fill(email)
        self.submit_button.click()