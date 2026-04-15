def generate_reasoning(context: dict) -> dict:
    context = context or {}

    market_sentiment = str(context.get("market_sentiment") or "mixed")
    conflict_detected = bool(context.get("conflict_detected", False))
    data_completeness = str(context.get("data_completeness") or "low")
    dominant_factors = context.get("dominant_factors") or []

    if dominant_factors:
        factor_labels = []
        for factor in dominant_factors[:3]:
            factor_name = str(factor.get("factor") or "factor")
            factor_value = str(factor.get("value") or factor.get("weight") or "")
            factor_labels.append(f"{factor_name}={factor_value}")
        factors_text = ", ".join(factor_labels)
    else:
        factors_text = "no dominant factors"

    reasoning = (
        f"Context indicates {market_sentiment} sentiment with {data_completeness} data completeness. "
        f"Key drivers: {factors_text}."
    )

    if conflict_detected:
        recommendation = "Hold a cautious stance until signal and news direction align."
    elif market_sentiment == "bullish":
        recommendation = "Bias is positive; consider selective long exposure with risk limits."
    elif market_sentiment == "bearish":
        recommendation = "Bias is negative; favor defensive positioning and tighter stops."
    elif market_sentiment == "incomplete":
        recommendation = "Wait for additional data before taking directional positions."
    else:
        recommendation = "Maintain neutral positioning while monitoring incoming updates."

    return {
        "reasoning": reasoning,
        "recommendation": recommendation,
    }
