def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def _resolve_confidence(market_sentiment: str, conflict_detected: bool) -> float:
    base_score = 0.8
    penalty_if_no_news = 0.4 if market_sentiment == "incomplete" else 0.0
    penalty_if_conflict = 0.25 if conflict_detected else 0.0
    return _clamp(base_score - penalty_if_no_news - penalty_if_conflict, 0.0, 1.0)


def _resolve_risk_level(market_sentiment: str, conflict_detected: bool) -> str:
    if conflict_detected:
        return "high"
    if market_sentiment == "incomplete":
        return "medium"
    return "low"


def _resolve_market_outlook(market_sentiment: str) -> str:
    if market_sentiment in {"bullish", "bearish"}:
        return market_sentiment
    return "neutral"


def _build_warnings(market_sentiment: str, conflict_detected: bool, data_completeness: str) -> list[str]:
    warnings = []
    if market_sentiment == "incomplete":
        warnings.append("News data unavailable; context is incomplete.")
    if conflict_detected:
        warnings.append("Conflicting market and news signals detected.")
    if data_completeness == "low" and market_sentiment != "incomplete":
        warnings.append("Limited news coverage may reduce reliability.")
    return warnings


def generate_decision(signals: dict, context: dict, reasoning: dict) -> dict:
    signals = signals or {}
    context = context or {}
    reasoning = reasoning or {}

    market_sentiment = str(context.get("market_sentiment") or "mixed")
    conflict_detected = bool(context.get("conflict_detected", False))
    data_completeness = str(context.get("data_completeness") or "low")
    confidence = _resolve_confidence(market_sentiment, conflict_detected)
    risk_level = _resolve_risk_level(market_sentiment, conflict_detected)
    market_outlook = _resolve_market_outlook(market_sentiment)
    warnings = _build_warnings(market_sentiment, conflict_detected, data_completeness)

    return {
        "market_outlook": market_outlook,
        "confidence": round(confidence, 4),
        "signals": signals,
        "dominant_factors": context.get("dominant_factors", []),
        "reasoning": str(reasoning.get("reasoning") or ""),
        "risk_level": risk_level,
        "warnings": warnings,
    }
