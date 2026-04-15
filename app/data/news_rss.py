DEFAULT_RSS_URL = "https://feeds.reuters.com/reuters/businessNews"


def fetch_news() -> list[dict]:
    try:
        import feedparser
    except ImportError:
        return []

    parsed_feed = feedparser.parse(DEFAULT_RSS_URL)

    if getattr(parsed_feed, "bozo", False):
        return []

    items = []
    for entry in getattr(parsed_feed, "entries", [])[:10]:
        title = getattr(entry, "title", "") or ""
        summary = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
        published = getattr(entry, "published", "") or getattr(entry, "updated", "") or ""

        items.append(
            {
                "title": title,
                "summary": summary,
                "published_date": published,
            }
        )

    return items
