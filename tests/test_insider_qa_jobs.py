import pytest

from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.open_positions_page import OpenPositionsPage


@pytest.mark.ui
def test_insider_qa_jobs_flow(driver):
    # 1) Home
    home = HomePage(driver)
    home.load()
    assert home.is_opened(), "Insider home page is not opened"
    #
    # 2) Company =-> Careers, validate blocks
    home.go_to_careers()
    careers = CareersPage(driver)
    assert careers.is_opened(), "Careers page is not opened"
    careers.verify_blocks()
    #
    # 3) QA page => See all QA jobs -> filter Istanbul + QA -> jobs list present
    jobs_page = OpenPositionsPage(driver)
    jobs_page.open_qa_page()
    jobs_page.click_see_all_qa_jobs()
    jobs_page.apply_filters()

    jobs = jobs_page.get_jobs()
    assert len(jobs) > 0, "Jobs list is empty after applying filters"
    #
    # # 4) Validate each job contains required fields (position/department/location)
    for j in jobs:
        assert "quality assurance" in j.position.lower(), f"Position does not contain Quality Assurance: {j.position}"
        assert "quality assurance" in j.department.lower(), f"Department does not contain Quality Assurance: {j.department}"

        loc = j.location.lower()
        assert "istanbul" in loc, f"Location is not Istanbul: {j.location}"
        assert any(x in loc for x in ["turkey", "turkiye", "türkiye"]), f"Country is not Turkey/Turkiye: {j.location}"

    # 5) View Role -> Lever
    jobs_page.click_first_view_role()
    jobs_page.assert_redirected_to_lever()
