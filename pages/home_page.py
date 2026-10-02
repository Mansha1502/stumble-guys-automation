from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.play_now_button = page.get_by_role("button", name="Play Now!")

    def click_play_now(self):
        self.play_now_button.click()