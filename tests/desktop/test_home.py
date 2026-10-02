import re

from playwright.sync_api import Page, expect

from pages.home_page import HomePage


def test_home_page_shows_play_button(page: Page, base_url: str):
    home_page = HomePage(page)

    home_page.navigate(base_url)
    home_page.accept_cookies()

    expect(page).to_have_url(re.compile(r"stumbleguys\.com"))
    expect(home_page.play_now_button).to_be_visible()