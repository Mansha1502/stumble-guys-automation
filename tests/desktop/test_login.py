import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from utils.config import TEST_EMAIL


def test_login_form_shows_email_option(page: Page, base_url: str):
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    login_page.accept_cookies()

    login_page.open_login_options()

    expect(login_page.email_option).to_be_visible()


def test_invalid_email_shows_format_error(page: Page, base_url: str):
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    login_page.accept_cookies()

    login_page.open_login_options()
    login_page.choose_email_login()
    login_page.enter_email("abc")

    expect(login_page.email_error).to_be_visible()


@pytest.mark.skipif(not TEST_EMAIL, reason="TEST_EMAIL is not set in .env")
def test_valid_email_opens_otp_screen(page: Page, base_url: str):
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    login_page.accept_cookies()

    login_page.open_login_options()
    login_page.choose_email_login()
    login_page.submit_email(TEST_EMAIL)

    expect(login_page.otp_inputs).to_have_count(6)


def test_saved_session_keeps_user_logged_in(logged_in_page: Page, base_url: str):
    login_page = LoginPage(logged_in_page)
    login_page.navigate(base_url)
    login_page.accept_cookies()

    login_page.open_account_menu()

    expect(login_page.logout_button).to_be_visible()
