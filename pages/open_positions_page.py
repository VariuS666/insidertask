from dataclasses import dataclass

from selenium.common import ElementClickInterceptedException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time



@dataclass
class JobCard:
    position: str
    department: str
    location: str


class OpenPositionsPage(BasePage):
    QA_URL = "https://useinsider.com/careers/quality-assurance/"

    SEE_ALL_QA_JOBS = (By.XPATH, "//a[normalize-space()='See all QA jobs']")

    # Open positions page filter dropdown
    FILTER_LOCATION = (By.XPATH, "//select[@id='filter-by-location']")
    FILTER_DEPARTMENT = (By.XPATH, "//*[self::button or self::div][contains(., 'All department') or contains(., 'Department')]")

    ISTANBUL_OPTION = (By.XPATH, "//option[@class='job-location istanbulturkiye']")
    QA_OPTION = (By.XPATH, "//*[self::li or self::div or self::span][contains(., 'Quality Assurance')]")

    # Job card and view role
    JOB_CARDS = (By.XPATH, "//*[self::div or self::li][.//*[contains(., 'View Role') or contains(., 'Apply')]]")
    VIEW_ROLE_BUTTON = (By.XPATH, ".//*[self::a or self::button][contains(., 'View Role')]")

    def open_qa_page(self):
        self.open(self.QA_URL)
        self.accept_cookies_if_present()
        self.wait_visible((By.XPATH, "//*[contains(., 'Quality Assurance')]"), timeout=15)

    def click_see_all_qa_jobs(self):
        self.accept_cookies_if_present()

        btn = self.wait_clickable(self.SEE_ALL_QA_JOBS)

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)

        # Normal click
        try:
            btn.click()
        except Exception:
            # Fallback: JS click
            self.driver.execute_script("arguments[0].click();", btn)

        #if new tab
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])

        self.wait.until(lambda d: d.current_url.lower() != self.QA_URL.lower())
        self.wait.until(lambda d: ("open" in d.current_url.lower()) or ("jobs" in d.current_url.lower()))

        self.wait_visible(self.FILTER_LOCATION, timeout=25)
        self.wait_visible(self.FILTER_DEPARTMENT, timeout=25)


    def apply_filters(self):
        self.accept_cookies_if_present()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[contains(., 'View Role')]")
            ),
            message="View Role buttons did not load before applying filters"
        )

        location_select = self.wait_visible(self.FILTER_LOCATION, timeout=25)
        Select(location_select).select_by_visible_text("Istanbul, Turkiye")

        dept_select_locator = (By.ID, "filter-by-department")
        if self.is_present(dept_select_locator, timeout=3):
            dept_select = self.wait_visible(dept_select_locator, timeout=10)
            Select(dept_select).select_by_visible_text("Quality Assurance")

        def filtered_results_loaded(driver):
            cards = driver.find_elements(By.XPATH, "//a[contains(., 'View Role')]/ancestor::div[1]")
            if not cards:
                return False

            text = " ".join(c.text.lower() for c in cards[:3])
            return (
                    "istanbul" in text
                    and "quality assurance" in text
                    and any(x in text for x in ["turkey", "turkiye", "türkiye"])
            )

        self.wait.until(filtered_results_loaded)


    def get_jobs(self) -> list[JobCard]:
        view_role_buttons = self.wait_all_visible(
            (By.XPATH, "//a[normalize-space()='View Role' or contains(., 'View Role')]"),
            timeout=25
        )

        jobs: list[JobCard] = []

        for btn in view_role_buttons:
            card = btn.find_element(By.XPATH, "./ancestor::div[.//a[contains(., 'View Role')]][1]")

            lines = [l.strip() for l in card.text.splitlines() if l.strip()]

            #[0]=position, [1]=department, [2]=location
            position = lines[0] if len(lines) > 0 else ""
            department = lines[1] if len(lines) > 1 else ""
            location = lines[2] if len(lines) > 2 else ""

            jobs.append(JobCard(position=position, department=department, location=location))

        return jobs

    def click_first_view_role(self):
        self.accept_cookies_if_present()


        btn_locator = (By.XPATH, "(//a[contains(., 'View Role')])[1]")

        btn = self.wait_clickable(btn_locator, timeout=25)

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)

        try:
            btn.click()
        except ElementClickInterceptedException:

            self.driver.execute_script("arguments[0].click();", btn)

    def assert_redirected_to_lever(self):

        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])

        self.wait.until(lambda d: "lever.co" in d.current_url.lower())

        self.wait_visible(
            (By.XPATH, "//*[contains(., 'Apply for this job') or contains(., 'Submit your application')]"),
            timeout=20
        )