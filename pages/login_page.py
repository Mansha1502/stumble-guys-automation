from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.avatar_button = page.get_by_role("button", name="avatar")
        self.login_button = page.get_by_role("button", name="Login")
        self.logout_button = page.get_by_role("button", name="Logout")
        self.email_option = page.get_by_role("button", name="Continue with email")
        self.email_input = page.locator('[data-test-id="Input"]')
        self.submit_button = page.locator('[data-test-id="site-email-input-submit-button"]')
        self.email_error = page.get_by_text("The format of the provided email is invalid")
        self.otp_inputs = page.get_by_role("textbox")

    def open_login_options(self):
        self.avatar_button.click()
        self.login_button.click()

    def open_account_menu(self):
        self.avatar_button.click()

    def choose_email_login(self):
        self.email_option.click()

    def enter_email(self, email: str):
        self.email_input.fill(email)

    def submit_email(self, email: str):
        self.enter_email(email)
        self.submit_button.click()