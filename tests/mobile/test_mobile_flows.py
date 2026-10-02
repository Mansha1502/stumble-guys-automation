from pages.mobile.login_mobile_page import LoginMobilePage
from pages.mobile.shop_mobile_page import ShopMobilePage


def test_login_form_shows_email_option(mobile_driver, base_url):
    login_page = LoginMobilePage(mobile_driver)
    login_page.navigate(base_url)
    login_page.accept_cookies()

    login_page.open_login_options()

    assert login_page.is_email_option_visible(), "Email login option should be shown"


def test_invalid_email_shows_format_error(mobile_driver, base_url):
    login_page = LoginMobilePage(mobile_driver)
    login_page.navigate(base_url)
    login_page.accept_cookies()

    login_page.open_login_options()
    login_page.choose_email_login()
    login_page.enter_email("abc")

    assert login_page.is_email_error_visible(), "Invalid email should show a format error"


def test_logged_out_user_is_asked_to_log_in_when_buying(mobile_driver, base_url):
    shop_page = ShopMobilePage(mobile_driver)
    shop_page.open(base_url)
    shop_page.accept_cookies()

    shop_page.select_first_item()

    assert shop_page.is_login_prompt_visible(), "A visitor should be asked to log in before buying"