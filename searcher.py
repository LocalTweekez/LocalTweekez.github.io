"""Periodic DuckDuckGo searcher for master thesis positions."""

import json
import time
import os
from urllib.parse import urlparse

from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException


QUERY = (
    "master thesis positions in stockholm for computing engineering students with masters degree in machine learning"
)
OUTPUT_FILE = "search_results.json"
REFRESH_INTERVAL = 60


def perform_search() -> list[dict]:
    """Fetch results from DuckDuckGo and write them to OUTPUT_FILE.

    Returns:
        list[dict]: Simplified search results or cached/empty list on error.
    """
    # Clear proxy environment variables that may interfere with network access
    for proxy_var in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
        os.environ.pop(proxy_var, None)

    ddgs = DDGS(proxies=None, timeout=10)

    try:
        raw_results = list(ddgs.text(QUERY, max_results=10))
    except DuckDuckGoSearchException as exc:
        print(f"DuckDuckGo search failed: {exc}")
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                cached = json.load(f)
                print(f"Using cached results from {OUTPUT_FILE}")
                return cached
        return []
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
    return simplified


def main() -> None:
    while True:
        try:
            perform_search()
        except Exception as exc:
            print(f"Search failed: {exc}")
        time.sleep(REFRESH_INTERVAL)


if __name__ == "__main__":
    main()
