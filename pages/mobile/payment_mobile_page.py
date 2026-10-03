from selenium.webdriver.common.by import By

from pages.mobile.base_mobile_page import BaseMobilePage


class PaymentMobilePage(BaseMobilePage):
    PAYMENT_IFRAME = (By.CSS_SELECTOR, 'iframe[title="Stumble Guys - Payment platform"]')
    PAY_BUTTON = (By.XPATH, '//button[normalize-space()="Pay"]')

    def is_payment_form_open(self) -> bool:
        return self.is_visible(self.PAYMENT_IFRAME, timeout=30)

    def is_pay_button_visible(self) -> bool:
        frame = self.wait.until(lambda driver: self._first_visible(self.PAYMENT_IFRAME))
        self.driver.switch_to.frame(frame)
        try:
            return self.is_visible(self.PAY_BUTTON, timeout=30)
        finally:
            self.driver.switch_to.default_content()