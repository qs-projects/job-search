import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/jobs.db")


def initialize_database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            unique_id TEXT PRIMARY KEY,
            company TEXT NOT NULL,
            title TEXT NOT NULL,
            location TEXT,
            url TEXT NOT NULL,
            posted_date TEXT,
            first_seen TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def job_already_seen(unique_id: str) -> bool:
    connection = sqlite3.connect(DATABASE_PATH)

    result = connection.execute(
        "SELECT 1 FROM jobs WHERE unique_id = ?",
        (unique_id,)
    ).fetchone()

    connection.close()

    return result is not None


def save_job(job):
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        INSERT OR IGNORE INTO jobs
        (unique_id, company, title, location, url, posted_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        job.unique_id,
        job.company,
        job.title,
        job.location,
        job.url,
        job.posted_date
    ))

    connection.commit()
    connection.close()

