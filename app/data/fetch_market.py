from datetime import datetime, timezone


def fetch_market_data() -> dict:
    return {
        "index": "NIFTY",
        "price": 22450.35,
        "change": 0.42,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
