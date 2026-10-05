from src.scrapers import SCRAPERS


def main():

    for company, scraper_class in SCRAPERS.items():

        print()
        print("=" * 70)
        print(company)
        print("=" * 70)

        try:

            scraper = scraper_class()

            jobs = scraper.fetch_jobs()

            print(f"Found {len(jobs)} jobs")

            for job in jobs:

                print(
                    f"  {job.title}"
                    f" | {job.location}"
                    f" | {job.url}"
                )

        except Exception as error:

            print(
                f"ERROR: {type(error).__name__}: {error}"
            )


if __name__ == "__main__":
    main()

# blocking code for second phase of testing

"""
from src.scrapers import SCRAPERS
from src.filters import title_matches


KEYWORDS = [
    "epic",
    "analyst",
    "manager"
]


def main():

    for company, scraper_class in SCRAPERS.items():

        print()
        print("=" * 70)
        print(company)
        print("=" * 70)

        scraper = scraper_class()

        jobs = scraper.fetch_jobs()

        matches = [
            job
            for job in jobs
            if title_matches(
                job.title,
                KEYWORDS
            )
        ]

        for job in matches:

            print()
            print(f"TITLE:    {job.title}")
            print(f"LOCATION: {job.location}")
            print(f"URL:      {job.url}")


if __name__ == "__main__":
    main()

"""
