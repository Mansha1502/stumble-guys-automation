from urllib.parse import urlsplit

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.mobile.base_mobile_page import BaseMobilePage


class LoginMobilePage(BaseMobilePage):
    AVATAR_BUTTON = (By.XPATH, '//button[.//img[@alt="avatar"]]')
    LOGIN_BUTTON = (By.XPATH, '//button[normalize-space()="Login"]')
    LOGIN_HEADING = (By.XPATH, '//h3[normalize-space()="Login"]')
    EMAIL_OPTION = (By.XPATH, '//button[.//img[@alt="Email logo"]]')
    EMAIL_INPUT = (By.CSS_SELECTOR, '[data-test-id="Input"]')
    EMAIL_SUBMIT = (By.CSS_SELECTOR, '[data-test-id="site-email-input-submit-button"]')
    EMAIL_ERROR = (By.XPATH, '//*[contains(text(), "The format of the provided email is invalid")]')
    CONTINUE_BUTTON = (By.XPATH, '//button[normalize-space()="Continue"]')
    SINGLE_CHARACTER_INPUTS = (By.CSS_SELECTOR, 'input[maxlength="1"]')
    DIALOG_INPUTS = (By.XPATH, '//*[@role="dialog"]//input')
    CODE_CONFIRM = (By.CSS_SELECTOR, '[data-test-id="Button"]')

    def open_login_options(self):
        self.click(self.AVATAR_BUTTON)
        # The menu sometimes needs a second tap on a real phone
        if not self.is_visible(self.LOGIN_BUTTON, timeout=5):
            self.click(self.AVATAR_BUTTON)
        self.click(self.LOGIN_BUTTON)

    def choose_email_login(self):
        self.click(self.EMAIL_OPTION)

    def enter_email(self, email: str):
        self.type_text(self.EMAIL_INPUT, email)

    def submit_email(self, email: str):
        self.enter_email(email)
        self.click(self.EMAIL_SUBMIT)

    def continue_if_asked(self):
        # After the email, a sign-in screen can ask to confirm it before the code is sent
        if self.is_visible(self.CONTINUE_BUTTON, timeout=8):
            self.click(self.CONTINUE_BUTTON)

    def wait_for_code_screen(self):
        try:
            return self.wait.until(lambda driver: self._code_boxes())
        except TimeoutException:
            raise TimeoutException(f"Login code boxes did not appear. Phone shows: {self.describe_page()}")

    def describe_page(self) -> str:
        # Describes where the phone is and what it can see, never what was typed into the fields
        url = urlsplit(self.driver.current_url)
        parts = [f"page={url.netloc}{url.path}"]
        for box in self.driver.find_elements(By.TAG_NAME, "input"):
            if box.is_displayed():
                parts.append(f"input(type={box.get_attribute('type')}, maxlength={box.get_attribute('maxlength')})")
        for button in self.driver.find_elements(By.TAG_NAME, "button"):
            if button.is_displayed() and button.text.strip():
                parts.append(f"button({button.text.strip()!r})")
        parts.append(f"iframes={len(self.driver.find_elements(By.TAG_NAME, 'iframe'))}")
        return ", ".join(parts)

    def enter_code(self, code: str):
        for box, digit in zip(self.wait_for_code_screen(), code):
            box.send_keys(digit)

    def confirm_code(self):
        self.click(self.CODE_CONFIRM)

    def wait_until_logged_in(self):
        self.wait.until(lambda driver: not self._first_visible(self.LOGIN_HEADING))

    def is_email_option_visible(self) -> bool:
        return self.is_visible(self.EMAIL_OPTION)

    def is_email_error_visible(self) -> bool:
        return self.is_visible(self.EMAIL_ERROR)

    def _code_boxes(self):
        # Code boxes usually take one character each, so look for those first,
        # and fall back to the inputs inside the login dialog
        for locator in (self.SINGLE_CHARACTER_INPUTS, self.DIALOG_INPUTS):
            boxes = [box for box in self.driver.find_elements(*locator) if box.is_displayed()]
            if len(boxes) >= 6:
                return boxes[-6:]
        return False