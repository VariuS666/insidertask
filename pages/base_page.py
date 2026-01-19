from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    DEFAULT_TIMEOUT = 20

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def open(self, url: str):
        self.driver.get(url)

    def wait_visible(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_all_visible(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(
            EC.visibility_of_all_elements_located(locator)
        )

    def click(self, locator):
        self.wait_clickable(locator).click()

    def get_text(self, locator) -> str:
        return self.wait_visible(locator).text.strip()

    def is_present(self, locator, timeout=3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

    def accept_cookies_if_present(self):
        try:
            accept_btn = self.wait_clickable(
                (By.ID, "wt-cli-accept-all-btn"),
                timeout=5
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                accept_btn
            )

            try:
                accept_btn.click()
            except Exception:
                # Fallback JS click
                self.driver.execute_script("arguments[0].click();", accept_btn)

        except TimeoutException:

            pass