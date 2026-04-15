import logging

from app.agents.reasoning_agent import generate_reasoning
from app.data.fetch_market import fetch_market_data
from app.data.fetch_news import fetch_news
from app.data.transform import clean_news
from app.engines.context_engine import generate_context
from app.engines.decision_engine import generate_decision
from app.engines.news_engine import analyze_news
from app.engines.signal_engine import generate_signals


logger = logging.getLogger(__name__)


def run_market_pipeline() -> dict:
    logger.info("Step 1: fetch market data")
    try:
        market_data = fetch_market_data()
    except Exception as error:
        logger.exception("Market data fetch failed: %s", error)
        market_data = {
            "index": "NIFTY",
            "price": 0.0,
            "change": 0.0,
            "timestamp": "",
        }

    logger.info("Step 2: fetch news")
    try:
        raw_news = fetch_news()
    except Exception as error:
        logger.exception("News fetch failed: %s", error)
        raw_news = []

    logger.info("Step 3: clean news")
    try:
        cleaned_news = clean_news(raw_news)
    except Exception as error:
        logger.exception("News transform failed: %s", error)
        cleaned_news = []

    logger.info("Step 4: generate signals")
    try:
        signals = generate_signals(market_data)
    except Exception as error:
        logger.exception("Signal engine failed: %s", error)
        signals = {
            "trend": "neutral",
            "momentum": "flat",
            "volatility": "low",
        }

    logger.info("Step 5: analyze news")
    try:
        news_analysis = analyze_news(cleaned_news)
    except Exception as error:
        logger.exception("News engine failed: %s", error)
        news_analysis = []

    logger.info("Step 6: generate context")
    try:
        context = generate_context(signals, news_analysis)
    except Exception as error:
        logger.exception("Context engine failed: %s", error)
        context = {
            "market_sentiment": "incomplete",
            "dominant_factors": [],
            "conflict_detected": False,
            "data_completeness": "low",
        }

    logger.info("Step 7: generate reasoning")
    try:
        reasoning = generate_reasoning(context)
    except Exception as error:
        logger.exception("Reasoning generation failed: %s", error)
        reasoning = {
            "reasoning": "Reasoning agent unavailable; returning rule-based fallback.",
            "recommendation": "Use caution until reasoning service recovers.",
        }

    logger.info("Step 8: generate decision")
    try:
        decision = generate_decision(signals, context, reasoning)
    except Exception as error:
        logger.exception("Decision engine failed: %s", error)
        decision = {
            "market_outlook": "neutral",
            "confidence": 0.0,
            "signals": signals,
            "dominant_factors": context.get("dominant_factors", []),
            "reasoning": str(reasoning.get("reasoning") or ""),
            "risk_level": "high",
            "warnings": ["Decision engine failure; fallback output used."],
        }

    logger.info("Step 9: pipeline complete")
    return decision
