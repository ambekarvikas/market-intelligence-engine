DEFAULT_RSS_URL = "https://feeds.reuters.com/reuters/businessNews"


def fetch_news() -> list[dict]:
    try:
        import feedparser
    except ImportError:
        return []

    parsed_feed = feedparser.parse(DEFAULT_RSS_URL)
    if getattr(parsed_feed, "bozo", False):
        return []

    news_items = []
    for entry in getattr(parsed_feed, "entries", [])[:10]:
        news_items.append(
            {
                "title": str(getattr(entry, "title", "") or "").strip(),
                "summary": str(
                    getattr(entry, "summary", "")
                    or getattr(entry, "description", "")
                    or ""
                ).strip(),
                "published": str(
                    getattr(entry, "published", "")
                    or getattr(entry, "updated", "")
                    or ""
                ).strip(),
            }
        )

    return news_items
