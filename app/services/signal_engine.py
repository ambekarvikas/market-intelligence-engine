def _parse_change_percent(change_value) -> float:
    if isinstance(change_value, (int, float)):
        return float(change_value)

    if not isinstance(change_value, str):
        return 0.0

    normalized = change_value.strip().replace("%", "")
    if not normalized:
        return 0.0

    try:
        return float(normalized)
    except ValueError:
        return 0.0


def _compute_trend(change_percent: float) -> str:
    if change_percent > 0.1:
        return "bullish"
    if change_percent < -0.1:
        return "bearish"
    return "neutral"


def _compute_momentum(change_percent: float) -> str:
    if change_percent >= 1.0:
        return "strong_up"
    if change_percent > 0.0:
        return "up"
    if change_percent <= -1.0:
        return "strong_down"
    if change_percent < 0.0:
        return "down"
    return "flat"


def generate_signals(market_data: dict) -> dict:
    market_data = market_data or {}
    change_percent = _parse_change_percent(market_data.get("change", 0.0))

    return {
        "index": market_data.get("index", ""),
        "timestamp": market_data.get("timestamp", ""),
        "trend": _compute_trend(change_percent),
        "momentum": _compute_momentum(change_percent),
    }
