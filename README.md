# Insider QA Automation Task

This project automates the Insider QA careers scenario using **Python + Selenium + Pytest**  
and follows **Page Object Model (POM)** principles.

## Covered Scenario
1. Verify Insider home page
2. Navigate to Company → Careers
3. Verify Careers page blocks:
   - Life at Insider
   - Teams
   - Locations
4. Open QA jobs page
5. Filter jobs by:
   - Location: Istanbul, Turkey
   - Department: Quality Assurance
6. Verify job list contents
7. Click "View Role" and verify redirection to Lever application page

##  Tech Stack
- Python 3
- Selenium WebDriver
- Pytest
- WebDriver Manager
- Page Object Model (POM)

##  How to Run

### Install dependencies
```bash
pip install -r requirements.txt
