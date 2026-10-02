import re

from playwright.sync_api import Page

from pages.base_page import BasePage

PRICE = re.compile(r"[₹$€£]")


class ShopPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.login_heading = page.get_by_role("heading", name="Login")
        self.login_prompt = page.get_by_role("button", name="Continue with email")
        self.price_buttons = page.get_by_role("button", name=PRICE)
        # Tailwind classes from the recorder, the only handle on the item card for now
        self.item_cards = page.locator(".w-full.cursor-pointer")
        self.item_modal = page.get_by_role("dialog")
        self.modal_price_button = self.item_modal.get_by_role("button", name=PRICE)

    def open(self, base_url: str):
        self.navigate(base_url.rstrip("/") + "/shop")

    def select_first_item(self):
        self.price_buttons.first.click()

    def open_first_item(self):
        self.item_cards.first.click()

    def continue_to_card_details(self):
        self.modal_price_button.click()