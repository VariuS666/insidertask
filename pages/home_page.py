from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://useinsider.com/"

    HERO = (By.XPATH, "//*[contains(., 'Be unstoppable') or contains(., 'customer engagement')]")


    COMPANY_MENU = (By.XPATH, "//a[normalize-space()='Company' or contains(., 'Company')]")
    CAREERS_LINK = (By.XPATH, "//a[contains(@href, '/careers') and (contains(., 'Careers') or contains(., 'We\\'re hiring') or contains(., 'hiring'))]")

    def load(self):
        self.open(self.URL)
        self.accept_cookies_if_present()

    def is_opened(self) -> bool:
        return self.is_present(self.HERO, timeout=15)

    def go_to_careers(self):
        # 1) Company menyusu varsa: click Company -> Careers
        if self.is_present(self.COMPANY_MENU, timeout=3):
            self.click(self.COMPANY_MENU)
            self.click(self.CAREERS_LINK)
            return

        # 2) fallback: birbaşa careers
        self.open("https://useinsider.com/careers/")
        self.accept_cookies_if_present()
