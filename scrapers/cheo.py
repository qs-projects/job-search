import requests

from src.models import Job
from src.scrapers.base import BaseScraper


class CheoScraper(BaseScraper):

    company = "CHEO"

    API_URL = (
        "https://cheo.wd10.myworkdayjobs.com/"
        "wday/cxs/cheo/External_Site/jobs"
    )

    BASE_URL = (
        "https://cheo.wd10.myworkdayjobs.com/"
        "en-US/External_Site"
    )

    def fetch_jobs(self) -> list[Job]:

        jobs = []
        offset = 0
        limit = 20

        while True:

            payload = {
                "appliedFacets": {},
                "limit": limit,
                "offset": offset,
                "searchText": ""
            }

            response = requests.post(
                self.API_URL,
                json=payload,
                timeout=30,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(compatible; JobWatch/1.0)"
                    )
                }
            )

            response.raise_for_status()

            data = response.json()

            postings = data.get("jobPostings", [])

            if not postings:
                break

            for posting in postings:

                title = posting.get("title", "").strip()

                external_path = posting.get("externalPath", "")

                url = (
                    "https://cheo.wd10.myworkdayjobs.com"
                    + external_path
                )

                location = None

                locations = posting.get("locationsText")

                if locations:
                    location = locations

                job_id = posting.get("bulletFields", [None])[0]

                jobs.append(
                    Job(
                        company=self.company,
                        title=title,
                        location=location,
                        url=url,
                        job_id=job_id
                    )
                )

            offset += limit

            total = data.get("total", 0)

            if offset >= total:
                break

        return jobs

