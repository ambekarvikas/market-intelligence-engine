import logging

from fastapi import FastAPI

from app.api.routes import router as market_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(title="Market Intelligence Engine API", version="1.0.0")
app.include_router(market_router)

