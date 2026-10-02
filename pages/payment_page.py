from playwright.sync_api import Page

from pages.base_page import BasePage

PAYMENT_IFRAME = 'iframe[title="Stumble Guys - Payment platform"]'
CARD_FRAME = "elements-inner-accessory-target"
EMAIL_FRAME = "text-input/email"


class PaymentPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    def _field(self, frame_url_part: str, name: str, timeout_ms: int = 30000):
        # The card fields sit in nested third-party frames (Stripe, Xsolla) that
        # can be replaced while loading, so we look the field up again each time
        waited = 0
        while waited < timeout_ms:
            for frame in self.page.frames:
                if frame_url_part not in frame.url:
                    continue
                field = frame.get_by_role("textbox", name=name)
                if field.count() and field.is_visible():
                    return field
            self.page.wait_for_timeout(500)
            waited += 500
        raise AssertionError(f"'{name}' field did not appear in the payment form")

    @property
    def card_number(self):
        return self._field(CARD_FRAME, "Card number")

    @property
    def expiry(self):
        return self._field(CARD_FRAME, "Expiration (MM/YY)")

    @property
    def security_code(self):
        return self._field(CARD_FRAME, "Security code")

    @property
    def email(self):
        return self._field(EMAIL_FRAME, "Email")

    @property
    def pay_button(self):
        # exact match, otherwise the PayPal option would match as well
        return self.page.frame_locator(PAYMENT_IFRAME).get_by_role("button", name="Pay", exact=True)