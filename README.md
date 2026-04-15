# Market Intelligence Engine

API-driven backend system for deterministic market analysis with explainable outputs.

## Objective

Build a market intelligence pipeline that:
- Processes market data and news
- Generates deterministic signals (no ML in core logic)
- Aggregates context with rule-based weighting
- Uses AI layer only for explanation
- Returns structured, confidence-scored decision output

## System Flow

ETL -> Signal Engine -> News Impact Engine -> Context Engine -> AI Reasoning -> Decision Engine -> API

## Project Structure

```text
app/
  data/
    fetch_market.py
    fetch_news.py
    transform.py
    loader.py

  engines/
    signal_engine.py
    news_engine.py
    context_engine.py
    decision_engine.py

  agents/
    reasoning_agent.py

  services/
    market_pipeline.py

  models/
    response_models.py

  api/
    routes.py

scripts/
  run_etl.py

main.py
```

## Setup

1. Create and activate a virtual environment (recommended)
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run ETL

```bash
python scripts/run_etl.py
```

Outputs are written to:
- `scripts/outputs/market_data.json`
- `scripts/outputs/cleaned_news.json`

## Run API

```bash
uvicorn main:app --reload
```

API endpoint:
- `GET /market-summary`

## Run Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Notes

- Core engines are deterministic and rule-based.
- API layer does not contain business logic; orchestration is in `run_market_pipeline()`.
- System includes fallbacks for missing/failed data sources.
