POSITIVE_KEYWORDS = {
    "gain",
    "growth",
    "rally",
    "surge",
    "rise",
    "strong",
    "profit",
    "upgrade",
    "beat",
    "expansion",
}

NEGATIVE_KEYWORDS = {
    "fall",
    "drop",
    "decline",
    "slump",
    "weak",
    "loss",
    "downgrade",
    "miss",
    "cut",
    "crisis",
}

IMPACT_HIGH_KEYWORDS = {
    "merger",
    "acquisition",
    "policy",
    "regulation",
    "ban",
    "rate hike",
    "interest rate",
    "lawsuit",
    "default",
}

IMPACT_MEDIUM_KEYWORDS = {
    "earnings",
    "forecast",
    "guidance",
    "investment",
    "partnership",
    "launch",
    "contract",
}

SECTOR_KEYWORDS = {
    "banking": {"bank", "banking", "lender", "loan", "rbi", "nbfc"},
    "IT": {"it", "software", "tech", "technology", "digital", "ai", "cloud"},
    "pharma": {"pharma", "drug", "biotech", "healthcare", "clinical"},
    "energy": {"energy", "oil", "gas", "power", "renewable", "solar"},
    "auto": {"auto", "automobile", "ev", "vehicle", "car", "two-wheeler"},
    "global": {"global", "fed", "us", "china", "europe", "geopolitical", "inflation"},
}


def _normalize_text(news: dict) -> str:
    text = news.get("text")
    if text:
        return str(text).lower()

    title = str(news.get("title") or "")
    summary = str(news.get("summary") or "")
    return f"{title} {summary}".strip().lower()


def _keyword_score(text: str, keywords: set[str]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def _detect_sentiment(text: str) -> str:
    positive_score = _keyword_score(text, POSITIVE_KEYWORDS)
    negative_score = _keyword_score(text, NEGATIVE_KEYWORDS)

    if positive_score > negative_score:
        return "positive"
    if negative_score > positive_score:
        return "negative"
    return "neutral"


def _detect_impact(text: str) -> str:
    if _keyword_score(text, IMPACT_HIGH_KEYWORDS) > 0:
        return "high"
    if _keyword_score(text, IMPACT_MEDIUM_KEYWORDS) > 0:
        return "medium"
    return "low"


def _detect_sector(text: str) -> str:
    best_sector = "general"
    best_score = 0

    for sector, keywords in SECTOR_KEYWORDS.items():
        score = _keyword_score(text, keywords)
        if score > best_score:
            best_sector = sector
            best_score = score

    return best_sector


def analyze_news(news_list: list) -> list[dict]:
    analyzed_items = []

    for raw_item in news_list or []:
        news = raw_item if isinstance(raw_item, dict) else {}
        normalized_text = _normalize_text(news)

        analyzed_items.append(
            {
                "text": str(news.get("text") or "").strip(),
                "timestamp": str(news.get("timestamp") or news.get("published_date") or "").strip(),
                "sentiment": _detect_sentiment(normalized_text),
                "impact": _detect_impact(normalized_text),
                "sector": _detect_sector(normalized_text),
            }
        )

    return analyzed_items
