from abc import ABC, abstractmethod
from src.models import Job


class BaseScraper(ABC):

    company: str

    @abstractmethod
    def fetch_jobs(self) -> list[Job]:
        """Return all currently available jobs."""
        raise NotImplementedError

