import sys
import types
import unittest
from unittest.mock import patch

from app.data.news_rss import fetch_news


class TestFetchNews(unittest.TestCase):
    def test_fetch_news_limits_to_top_10(self):
        entries = [
            types.SimpleNamespace(
                title=f"Title {index}",
                summary=f"Summary {index}",
                published=f"2026-04-15T00:00:{index:02d}Z",
            )
            for index in range(15)
        ]

        fake_feedparser = types.SimpleNamespace(
            parse=lambda _url: types.SimpleNamespace(bozo=False, entries=entries)
        )

        with patch.dict(sys.modules, {"feedparser": fake_feedparser}):
            result = fetch_news()

        self.assertEqual(len(result), 10)

    def test_fetch_news_handles_missing_fields_gracefully(self):
        entries = [
            types.SimpleNamespace(title="Only Title"),
            types.SimpleNamespace(description="Only Description", updated="2026-04-15"),
        ]

        fake_feedparser = types.SimpleNamespace(
            parse=lambda _url: types.SimpleNamespace(bozo=False, entries=entries)
        )

        with patch.dict(sys.modules, {"feedparser": fake_feedparser}):
            result = fetch_news()

        self.assertEqual(len(result), 2)
        self.assertEqual(set(result[0].keys()), {"title", "summary", "published_date"})
        self.assertEqual(result[0]["title"], "Only Title")
        self.assertEqual(result[0]["summary"], "")
        self.assertEqual(result[0]["published_date"], "")

        self.assertEqual(result[1]["title"], "")
        self.assertEqual(result[1]["summary"], "Only Description")
        self.assertEqual(result[1]["published_date"], "2026-04-15")


if __name__ == "__main__":
    unittest.main()
