POSITIVE_KEYWORDS = {
    "gain",
    "growth",
    "rally",
    "surge",
    "rise",
    "profit",
    "beat",
}

NEGATIVE_KEYWORDS = {
    "fall",
    "drop",
    "decline",
    "loss",
    "slump",
    "miss",
    "cut",
}

IMPACT_HIGH_KEYWORDS = {
    "policy",
    "regulation",
    "merger",
    "acquisition",
    "rate hike",
    "default",
}

IMPACT_MEDIUM_KEYWORDS = {
    "earnings",
    "guidance",
    "forecast",
    "investment",
    "launch",
}

SECTOR_KEYWORDS = {
    "banking": {"bank", "banking", "rbi", "loan", "lender", "nbfc"},
    "IT": {"it", "software", "technology", "tech", "digital", "cloud", "ai"},
    "global": {"global", "fed", "us", "china", "europe", "inflation"},
    "energy": {"oil", "gas", "power", "energy", "renewable"},
    "auto": {"auto", "automobile", "vehicle", "ev"},
}


def _count_keyword_hits(text: str, keywords: set[str]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def _classify_sentiment(text: str) -> str:
    positive_hits = _count_keyword_hits(text, POSITIVE_KEYWORDS)
    negative_hits = _count_keyword_hits(text, NEGATIVE_KEYWORDS)

    if positive_hits > negative_hits:
        return "positive"
    if negative_hits > positive_hits:
        return "negative"
    return "neutral"


def _classify_impact(text: str) -> str:
    if _count_keyword_hits(text, IMPACT_HIGH_KEYWORDS) > 0:
        return "high"
    if _count_keyword_hits(text, IMPACT_MEDIUM_KEYWORDS) > 0:
        return "medium"
    return "low"


def _classify_sector(text: str) -> str:
    best_sector = "etc"
    best_score = 0

    for sector, keywords in SECTOR_KEYWORDS.items():
        score = _count_keyword_hits(text, keywords)
        if score > best_score:
            best_sector = sector
            best_score = score

    return best_sector


def analyze_news(news_list: list) -> list[dict]:
    analysis_output = []

    for raw_news in news_list or []:
        news_item = raw_news if isinstance(raw_news, dict) else {}
        text = str(news_item.get("text") or "").lower()

        analysis_output.append(
            {
                "sentiment": _classify_sentiment(text),
                "impact": _classify_impact(text),
                "sector": _classify_sector(text),
            }
        )

    return analysis_output
