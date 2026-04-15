TREND_SCORES = {
    "bullish": 1.0,
    "neutral": 0.0,
    "bearish": -1.0,
}

MOMENTUM_SCORES = {
    "strong_up": 1.0,
    "up": 0.5,
    "flat": 0.0,
    "down": -0.5,
    "strong_down": -1.0,
}

SENTIMENT_SCORES = {
    "positive": 1.0,
    "neutral": 0.0,
    "negative": -1.0,
}

IMPACT_WEIGHTS = {
    "high": 1.5,
    "medium": 1.0,
    "low": 0.5,
}

SIGNAL_WEIGHT = 0.55
NEWS_WEIGHT = 0.45


def _sentiment_from_score(score: float) -> str:
    if score >= 0.25:
        return "bullish"
    if score <= -0.25:
        return "bearish"
    return "neutral"


def generate_context(signal_output: dict, news_impact_output: list) -> dict:
    signal_output = signal_output or {}
    news_impact_output = news_impact_output or []

    trend = str(signal_output.get("trend") or "neutral")
    momentum = str(signal_output.get("momentum") or "flat")

    trend_score = TREND_SCORES.get(trend, 0.0)
    momentum_score = MOMENTUM_SCORES.get(momentum, 0.0)

    signal_component = (trend_score * 0.7) + (momentum_score * 0.3)

    news_score_sum = 0.0
    total_impact_weight = 0.0
    sector_contributions = {}

    for item in news_impact_output:
        news_item = item if isinstance(item, dict) else {}
        sentiment = str(news_item.get("sentiment") or "neutral")
        impact = str(news_item.get("impact") or "low")
        sector = str(news_item.get("sector") or "general")

        sentiment_score = SENTIMENT_SCORES.get(sentiment, 0.0)
        impact_weight = IMPACT_WEIGHTS.get(impact, 0.5)
        contribution = sentiment_score * impact_weight

        news_score_sum += contribution
        total_impact_weight += impact_weight
        sector_contributions[sector] = sector_contributions.get(sector, 0.0) + contribution

    if total_impact_weight > 0:
        news_component = news_score_sum / total_impact_weight
    else:
        news_component = 0.0

    has_conflict = signal_component * news_component < 0
    if has_conflict and abs(signal_component - news_component) <= 0.35:
        overall_score = 0.0
    else:
        overall_score = (signal_component * SIGNAL_WEIGHT) + (news_component * NEWS_WEIGHT)

    dominant_factors = [
        {
            "factor": "signal_trend",
            "value": trend,
            "contribution": round(trend_score * 0.7 * SIGNAL_WEIGHT, 4),
        },
        {
            "factor": "signal_momentum",
            "value": momentum,
            "contribution": round(momentum_score * 0.3 * SIGNAL_WEIGHT, 4),
        },
    ]

    top_sectors = sorted(
        sector_contributions.items(),
        key=lambda row: abs(row[1]),
        reverse=True,
    )[:3]

    for sector, score in top_sectors:
        dominant_factors.append(
            {
                "factor": "news_sector",
                "value": sector,
                "contribution": round(score * NEWS_WEIGHT, 4),
            }
        )

    if has_conflict:
        dominant_factors.append(
            {
                "factor": "conflict",
                "value": "signal_vs_news",
                "contribution": round(-abs(signal_component - news_component) * 0.1, 4),
            }
        )

    dominant_factors = sorted(dominant_factors, key=lambda row: abs(row["contribution"]), reverse=True)

    return {
        "overall_market_sentiment": _sentiment_from_score(overall_score),
        "dominant_factors": dominant_factors,
        "scores": {
            "signal": round(signal_component, 4),
            "news": round(news_component, 4),
            "overall": round(overall_score, 4),
        },
        "conflict_detected": has_conflict,
    }
