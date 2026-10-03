from selenium.webdriver.common.by import By

from pages.mobile.base_mobile_page import BaseMobilePage


class ShopMobilePage(BaseMobilePage):
    # Class name from the page, the hashed part after it changes between releases
    PRICE_BUTTON = (By.CSS_SELECTOR, '[class*="Card_card__price_button"]')
    # Tailwind classes, the only handle on the item card for now
    ITEM_CARD = (By.CSS_SELECTOR, ".w-full.cursor-pointer")
    MODAL_PRICE_BUTTON = (
        By.XPATH,
        '//*[@role="dialog"]//button[contains(., "₹") or contains(., "$") or contains(., "€") or contains(., "£")]',
    )
    LOGIN_HEADING = (By.XPATH, '//h3[normalize-space()="Login"]')
    EMAIL_OPTION = (By.XPATH, '//button[.//img[@alt="Email logo"]]')

    def open(self, base_url: str):
        self.navigate(base_url.rstrip("/") + "/shop")

    def select_first_item(self):
        self.click(self.PRICE_BUTTON)

    def open_first_item(self):
        self.click(self.ITEM_CARD)

    def continue_to_card_details(self):
        self.click(self.MODAL_PRICE_BUTTON)

    def is_login_prompt_visible(self) -> bool:
        return self.is_visible(self.LOGIN_HEADING) and self.is_visible(self.EMAIL_OPTION)