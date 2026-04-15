from datetime import datetime, timezone


def _current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def fetch_nifty_data() -> dict:
    return {
        "index": "NIFTY 50",
        "price": 22450.35,
        "change": "+0.42%",
        "timestamp": _current_timestamp(),
    }
