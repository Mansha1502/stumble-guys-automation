from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    def is_stumble_guys_visible(self):
        return self.page.get_by_text("Stumble Guys").first.is_visible()

    def hover_profile_icon(self):
        self.page.get_by_alt_text("avatar").hover()