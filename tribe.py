import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from src.models import Job
from src.scrapers.base import BaseScraper


class TribeMedicalScraper(BaseScraper):

    company = "Tribe Medical"

    URL = "https://tribemedical.com/careers/"

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

            url = urljoin(self.URL, href)

            # Only consider links that look job-related.
            text = f"{title} {href}".lower()

            if not any(
                word in text
                for word in (
                    "career",
                    "job",
                    "position",
                    "apply",
                    "employment"
                )
            ):
                continue

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

