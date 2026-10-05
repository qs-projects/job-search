from src.scrapers import SCRAPERS


for company, scraper_class in SCRAPERS.items():

    scraper = scraper_class()

    jobs = scraper.fetch_jobs()

    print(
        f"{company}: "
        f"{len(jobs)} jobs found"
    )
