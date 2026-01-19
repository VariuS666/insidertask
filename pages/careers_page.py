from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CareersPage(BasePage):
    URL = "https://useinsider.com/careers/"

    # Task: Locations, Teams, Life at Insider blokları
    LIFE_AT = (By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'life at insider')]")
    TEAMS = (By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'explore open roles') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'teams')]")
    LOCATIONS = (By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'our locations') or contains(., 'locations')]")

    def is_opened(self) -> bool:
        return "careers" in self.driver.current_url.lower()

    def verify_blocks(self):
        self.accept_cookies_if_present()
        assert self.wait_visible(self.LIFE_AT), "Life at Insider block is not visible"
        assert self.wait_visible(self.TEAMS), "Teams / Explore open roles block is not visible"
        assert self.wait_visible(self.LOCATIONS), "Locations block is not visible"
