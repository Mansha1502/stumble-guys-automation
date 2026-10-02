from selenium.webdriver.common.by import By

from pages.mobile.base_mobile_page import BaseMobilePage


class LoginMobilePage(BaseMobilePage):
    AVATAR_BUTTON = (By.XPATH, '//button[.//img[@alt="avatar"]]')
    LOGIN_BUTTON = (By.XPATH, '//button[normalize-space()="Login"]')
    EMAIL_OPTION = (By.XPATH, '//button[.//img[@alt="Email logo"]]')
    EMAIL_INPUT = (By.CSS_SELECTOR, '[data-test-id="Input"]')
    EMAIL_ERROR = (By.XPATH, '//*[contains(text(), "The format of the provided email is invalid")]')

    def open_login_options(self):
        self.click(self.AVATAR_BUTTON)
        self.click(self.LOGIN_BUTTON)

    def choose_email_login(self):
        self.click(self.EMAIL_OPTION)

    def enter_email(self, email: str):
        self.type_text(self.EMAIL_INPUT, email)

    def is_email_option_visible(self) -> bool:
        return self.is_visible(self.EMAIL_OPTION)

    def is_email_error_visible(self) -> bool:
        return self.is_visible(self.EMAIL_ERROR)