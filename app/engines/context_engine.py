SECTOR_WEIGHTS = {
    "banking": 0.4,
    "IT": 0.2,
    "global": 0.6,
}

SENTIMENT_SCORES = {
    "positive": 1.0,
    "neutral": 0.0,
    "negative": -1.0,
}

IMPACT_WEIGHTS = {
    "high": 1.0,
    "medium": 0.7,
    "low": 0.4,
}


def _signal_score(signals: dict) -> float:
    trend = str((signals or {}).get("trend") or "neutral")
    if trend == "bullish":
        return 1.0
    if trend == "bearish":
        return -1.0
    return 0.0


def _empty_context_output() -> dict:
    return {
        "market_sentiment": "incomplete",
        "dominant_factors": [
            {
                "factor": "news_availability",
                "value": "missing",
                "weight": -0.4,
            }
        ],
        "conflict_detected": False,
        "data_completeness": "low",
    }


def _extract_news_fields(item: dict) -> tuple[str, str, str]:
    news_item = item if isinstance(item, dict) else {}
    sentiment = str(news_item.get("sentiment") or "neutral")
    impact = str(news_item.get("impact") or "low")
    sector = str(news_item.get("sector") or "etc")
    return sentiment, impact, sector


def _compute_news_components(news_analysis: list) -> dict:
    positive_count = 0
    negative_count = 0
    weighted_news_sum = 0.0
    total_weight = 0.0
    factor_contributions = {}

    for item in news_analysis:
        sentiment, impact, sector = _extract_news_fields(item)

        if sentiment == "positive":
            positive_count += 1
        if sentiment == "negative":
            negative_count += 1

        sentiment_score = SENTIMENT_SCORES.get(sentiment, 0.0)
        impact_weight = IMPACT_WEIGHTS.get(impact, 0.4)
        sector_weight = SECTOR_WEIGHTS.get(sector, 0.3)
        contribution = sentiment_score * impact_weight * sector_weight

        weighted_news_sum += contribution
        total_weight += impact_weight * sector_weight
        factor_key = f"{sector}:{sentiment}"
        factor_contributions[factor_key] = factor_contributions.get(factor_key, 0.0) + contribution

    news_score = weighted_news_sum / total_weight if total_weight > 0 else 0.0
    return {
        "positive_count": positive_count,
        "negative_count": negative_count,
        "news_score": news_score,
        "factor_contributions": factor_contributions,
    }


def _detect_conflict(signal_score: float, positive_count: int, negative_count: int) -> bool:
    if positive_count > 0 and negative_count > 0:
        return True
    if signal_score > 0 and negative_count > 0:
        return True
    if signal_score < 0 and positive_count > 0:
        return True
    return False


def _resolve_market_sentiment(combined_score: float, conflict_detected: bool) -> str:
    if conflict_detected and abs(combined_score) < 0.35:
        return "mixed"
    if combined_score > 0.2:
        return "bullish"
    if combined_score < -0.2:
        return "bearish"
    return "mixed"


def _resolve_data_completeness(news_count: int) -> str:
    if news_count >= 5:
        return "high"
    if news_count >= 2:
        return "medium"
    return "low"


def _build_dominant_factors(factor_contributions: dict, signals: dict, signal_score: float) -> list[dict]:
    dominant_factors = [
        {
            "factor": key,
            "weight": round(value, 4),
        }
        for key, value in sorted(
            factor_contributions.items(),
            key=lambda row: abs(row[1]),
            reverse=True,
        )[:3]
    ]

    dominant_factors.append(
        {
            "factor": "signal_trend",
            "value": str(signals.get("trend") or "neutral"),
            "weight": round(signal_score * 0.6, 4),
        }
    )

    return dominant_factors


def generate_context(signals: dict, news_analysis: list) -> dict:
    signals = signals or {}
    news_analysis = news_analysis or []

    if not news_analysis:
        return _empty_context_output()

    signal_score = _signal_score(signals)
    news_components = _compute_news_components(news_analysis)
    positive_count = news_components["positive_count"]
    negative_count = news_components["negative_count"]
    news_score = news_components["news_score"]
    factor_contributions = news_components["factor_contributions"]

    combined_score = (signal_score * 0.6) + (news_score * 0.4)
    conflict_detected = _detect_conflict(signal_score, positive_count, negative_count)
    market_sentiment = _resolve_market_sentiment(combined_score, conflict_detected)
    data_completeness = _resolve_data_completeness(len(news_analysis))
    dominant_factors = _build_dominant_factors(factor_contributions, signals, signal_score)

    return {
        "market_sentiment": market_sentiment,
        "dominant_factors": dominant_factors,
        "conflict_detected": conflict_detected,
        "data_completeness": data_completeness,
    }
