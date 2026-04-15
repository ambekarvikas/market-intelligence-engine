def _build_factor_text(factors: list[dict]) -> str:
    if not factors:
        return "No dominant factors were provided."

    top_factors = factors[:3]
    parts = []
    for factor in top_factors:
        factor_name = str(factor.get("factor") or "factor")
        factor_value = str(factor.get("value") or "unknown")
        parts.append(f"{factor_name}={factor_value}")

    return ", ".join(parts)


def _build_recommendation(sentiment: str, has_conflict: bool) -> str:
    if has_conflict:
        return "Hold and wait for clearer alignment between market signals and news flow."

    if sentiment == "bullish":
        return "Consider a cautious long bias with disciplined risk controls."
    if sentiment == "bearish":
        return "Consider a defensive stance and reduce high-risk exposure."
    return "Stay neutral and monitor incoming data before taking directional positions."


def generate_reasoning(context: dict) -> dict:
    context = context or {}

    sentiment = str(context.get("overall_market_sentiment") or "neutral")
    dominant_factors = context.get("dominant_factors") or []
    has_conflict = bool(context.get("conflict_detected", False))

    factor_text = _build_factor_text(dominant_factors)
    conflict_text = "Conflict detected between signal and news components." if has_conflict else "No major conflicts detected."

    explanation = (
        f"Overall sentiment is {sentiment}. "
        f"Primary drivers: {factor_text}. "
        f"{conflict_text}"
    )

    return {
        "explanation_text": explanation,
        "recommendation": _build_recommendation(sentiment, has_conflict),
    }
