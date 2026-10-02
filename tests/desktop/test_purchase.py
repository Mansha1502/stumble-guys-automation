from playwright.sync_api import Page, expect

from pages.payment_page import PaymentPage
from pages.shop_page import ShopPage


def test_logged_out_user_is_asked_to_log_in_when_buying(page: Page, base_url: str):
    shop_page = ShopPage(page)

    shop_page.open(base_url)
    shop_page.accept_cookies()
    shop_page.select_first_item()

    expect(shop_page.login_heading).to_be_visible()
    expect(shop_page.login_prompt).to_be_visible()


def test_logged_in_user_reaches_card_details_without_paying(logged_in_page: Page, base_url: str):
    shop_page = ShopPage(logged_in_page)
    payment_page = PaymentPage(logged_in_page)

    shop_page.open(base_url)
    shop_page.accept_cookies()

    expect(shop_page.price_buttons.first).to_be_visible()
    expect(shop_page.login_prompt).to_have_count(0)

    shop_page.open_first_item()
    shop_page.continue_to_card_details()

    # The payment form is a third-party iframe, so it can take a while to load
    expect(payment_page.card_number).to_be_visible(timeout=20000)
    expect(payment_page.expiry).to_be_visible()
    expect(payment_page.security_code).to_be_visible()
    expect(payment_page.email).to_be_visible()
    expect(payment_page.pay_button).to_be_visible()
    # Stop here: no card details are typed and the pay button is never clicked