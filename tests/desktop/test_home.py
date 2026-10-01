from playwright.sync_api import Page

from pages.home_page import HomePage


def test_stumble_guys_homepage(page: Page, base_url: str):
    home_page = HomePage(page)

    home_page.navigate(base_url)

    assert home_page.get_title() != ""
    assert home_page.is_stumble_guys_visible()