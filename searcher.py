"""Periodic DuckDuckGo searcher for master thesis positions."""

import json
import time
from urllib.parse import urlparse

from duckduckgo_search import DDGS


QUERY = (
    "master thesis positions in stockholm for computing engineering students with masters degree in machine learning"
)
OUTPUT_FILE = "search_results.json"
REFRESH_INTERVAL = 60


def perform_search() -> None:
    """Fetch results from DuckDuckGo and write them to OUTPUT_FILE."""
    ddgs = DDGS()

    raw_results = list(ddgs.text(QUERY, max_results=10))
    simplified = []
    for r in raw_results:
        parsed = urlparse(r.get("href", ""))
        host = parsed.hostname or ""
        parts = host.split(".")
        company = parts[-2] if len(parts) >= 2 else host
        simplified.append(
            {
                "title": r.get("title"),
                "href": r.get("href"),
                "body": r.get("body"),
                "company": company.capitalize(),
            }
        )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(simplified, f, ensure_ascii=False, indent=2)
    print(f"Updated {OUTPUT_FILE} with {len(simplified)} results")


def main() -> None:
    while True:
        try:
            perform_search()
        except Exception as exc:
            print(f"Search failed: {exc}")
        time.sleep(REFRESH_INTERVAL)


if __name__ == "__main__":
    main()
