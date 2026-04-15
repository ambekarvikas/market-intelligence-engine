from fastapi import APIRouter

from app.models.response_models import MarketSummaryResponseModel
from app.services.market_pipeline import run_market_pipeline


router = APIRouter()


@router.get("/market-summary")
def get_market_summary() -> MarketSummaryResponseModel:
    decision_output = run_market_pipeline(use_ai=False)
    return MarketSummaryResponseModel(**decision_output)
