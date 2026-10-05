import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from src.models import Job
from src.scrapers.base import BaseScraper


class RoyalScraper(BaseScraper):

    company = "The Royal"

    URL = "https://jobs.jobvite.com/theroyal/"

    def fetch_jobs(self) -> list[Job]:

        response = requests.get(
            self.URL,
            timeout=30,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(compatible; JobWatch/1.0)"
                )
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        jobs = []

        for link in soup.find_all("a", href=True):

            title = link.get_text(" ", strip=True)

            href = link["href"]

            if not title:
                continue

            # Jobvite job links normally contain /job/
            if "/job/" not in href:
                continue

            url = urljoin(self.URL, href)

            jobs.append(
                Job(
                    company=self.company,
                    title=title,
                    location=None,
                    url=url
                )
            )

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

