def generate_signals(market_data: dict) -> dict:
    market_data = market_data or {}
    change_value = market_data.get("change", 0.0)

    try:
        change = float(change_value)
    except (TypeError, ValueError):
        change = 0.0

    if change > 0:
        trend = "bullish"
        momentum = "up"
    elif change < 0:
        trend = "bearish"
        momentum = "down"
    else:
        trend = "neutral"
        momentum = "flat"

    absolute_change = abs(change)
    if absolute_change < 0.5:
        volatility = "low"
    elif absolute_change < 1.5:
        volatility = "medium"
    else:
        volatility = "high"

    return {
        "trend": trend,
        "momentum": momentum,
        "volatility": volatility,
    }
