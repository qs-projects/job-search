from playwright.sync_api import sync_playwright

from src.models import Job
from src.scrapers.base import BaseScraper


class OttawaHospitalScraper(BaseScraper):

    company = "The Ottawa Hospital"

    URL = (
        "https://jobposting.ottawahospital.on.ca/"
        "psc/jobposting/EMPLOYEE/HRMS/c/"
        "HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL"
        "?Action=U&FOCUS=Applicant"
        "&Page=HRS_APP_SCHJOB_FL"
        "&SiteId=2"
    )

    def fetch_jobs(self) -> list[Job]:

        jobs = []

        with sync_playwright() as playwright:

            browser = playwright.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            page.goto(
                self.URL,
                wait_until="networkidle",
                timeout=60000
            )

            # Give PeopleSoft time to finish rendering.
            page.wait_for_timeout(3000)

            # We deliberately inspect links instead of
            # depending on one particular CSS class.
            links = page.locator("a").all()

            for link in links:

                try:
                    title = link.inner_text().strip()
                    href = link.get_attribute("href")
                except Exception:
                    continue

                if not title or not href:
                    continue

                title_lower = title.lower()

                # PeopleSoft job links normally contain
                # the job opening/application information.
                if not any(
                    keyword in title_lower
                    for keyword in (
                        "analyst",
                        "manager",
                        "epic"
                    )
                ):
                    continue

                if "job" not in href.lower():
                    continue

                if href.startswith("/"):

                    href = (
                        "https://jobposting.ottawahospital.on.ca"
                        + href
                    )

                jobs.append(
                    Job(
                        company=self.company,
                        title=title,
                        location="Ottawa, Ontario",
                        url=href
                    )
                )

            browser.close()

        return self._deduplicate(jobs)

    @staticmethod
    def _deduplicate(jobs: list[Job]) -> list[Job]:

        seen = set()
        result = []

        for job in jobs:

            if job.url in seen:
                continue

            seen.add(job.url)
            result.append(job)

        return result
