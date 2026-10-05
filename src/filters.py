import re


def title_matches(
    title: str,
    include_keywords: list[str],
    exclude_keywords: list[str] | None = None
) -> bool:

    exclude_keywords = exclude_keywords or []

    title = title.lower()

    # Exclusions take priority.
    for keyword in exclude_keywords:

        if keyword.lower() in title:
            return False

    # Then check inclusions.
    for keyword in include_keywords:

        if keyword.lower() in title:
            return True

    return False

from src.filters import title_matches


KEYWORDS = [
    "epic",
    "analyst",
    "manager"
]


if title_matches(job.title, KEYWORDS):
    print("MATCH:", job.title)

