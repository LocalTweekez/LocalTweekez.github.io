import json
import time
from duckduckgo_search import DDGS

QUERY = (
    "master thesis positions in stockholm for computing engineering students with masters degree in machine learning"
)
OUTPUT_FILE = "search_results.json"


def perform_search():
    ddgs = DDGS()
    results = list(ddgs.text(QUERY, max_results=10))
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def main():
    while True:
        try:
            perform_search()
        except Exception as exc:
            print(f"Search failed: {exc}")
        time.sleep(60)


if __name__ == "__main__":
    main()
