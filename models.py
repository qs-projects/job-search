from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    company: str
    title: str
    location: Optional[str]
    url: str
    posted_date: Optional[str] = None
    job_id: Optional[str] = None

    @property
    def unique_id(self) -> str:
        if self.job_id:
            return f"{self.company}:{self.job_id}"

        return f"{self.company}:{self.url}"
