from pages.mobile.login_mobile_page import LoginMobilePage
from pages.mobile.payment_mobile_page import PaymentMobilePage
from pages.mobile.shop_mobile_page import ShopMobilePage
from utils.config import TEST_EMAIL


def ask_for_login_code() -> str:
    code = input("\nEnter the 6-digit login code from your email: ").strip()
    assert code.isdigit() and len(code) == 6, "The login code must be 6 digits"
    return code


def test_logged_in_user_reaches_card_details_on_ios(interactive_mobile_driver, base_url):
    login_page = LoginMobilePage(interactive_mobile_driver)
    shop_page = ShopMobilePage(interactive_mobile_driver)
    payment_page = PaymentMobilePage(interactive_mobile_driver)

    login_page.navigate(base_url)
    login_page.accept_cookies()
    login_page.open_login_options()
    login_page.choose_email_login()
    login_page.submit_email(TEST_EMAIL)
    login_page.continue_if_asked()

    # Only ask for the code once the code screen is really there
    login_page.wait_for_code_screen()
    login_page.enter_code(ask_for_login_code())
    login_page.confirm_code()
    login_page.wait_until_logged_in()

    shop_page.open(base_url)
    shop_page.open_first_item()
    shop_page.continue_to_card_details()

    assert payment_page.is_payment_form_open(), "The payment form should open for a logged-in user"
    assert payment_page.is_pay_button_visible(), "The Pay button should be shown on the payment form"
    # Stop here: no card details are typed and Pay is never clicked