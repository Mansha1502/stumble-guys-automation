from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

COOKIE_OVERLAY = (By.ID, "uc-overlay")

# Looks for a button with this text in the page and inside any shadow DOM
CLICK_BUTTON_JS = """
const label = arguments[0];
function search(root) {
  for (const el of root.querySelectorAll('*')) {
    if (el.tagName === 'BUTTON' && el.textContent.trim() === label) {
      el.click();
      return true;
    }
    if (el.shadowRoot && search(el.shadowRoot)) {
      return true;
    }
  }
  return false;
}
return search(document);
"""


class BaseMobilePage:

    def __init__(self, driver, timeout: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def navigate(self, url: str):
        self.driver.get(url)

    def _first_visible(self, locator):
        # The page can hold a hidden copy of an element (for example a desktop
        # version of a menu), so we pick the first one that is actually displayed
        for element in self.driver.find_elements(*locator):
            try:
                if element.is_displayed():
                    return element
            except StaleElementReferenceException:
                continue
        return False

    def click(self, locator):
        try:
            self.wait.until(lambda driver: self._first_visible(locator)).click()
        except TimeoutException:
            total = len(self.driver.find_elements(*locator))
            raise TimeoutException(f"No visible element for {locator}, {total} match(es) in the page")

    def type_text(self, locator, text: str):
        field = self.wait.until(lambda driver: self._first_visible(locator))
        field.clear()
        field.send_keys(text)

    def is_visible(self, locator, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver: self._first_visible(locator))
            return True
        except TimeoutException:
            return False

    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script(CLICK_BUTTON_JS, "Accept All")
            )
        except TimeoutException:
            return

        # The banner fades out, and taps landing on it would not reach the page
        try:
            WebDriverWait(self.driver, 5).until(lambda driver: not self._first_visible(COOKIE_OVERLAY))
        except TimeoutException:
            pass