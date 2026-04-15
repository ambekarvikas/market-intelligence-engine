from pydantic import BaseModel


class SignalOutputModel(BaseModel):
    trend: str
    momentum: str
    volatility: str


class DominantFactorModel(BaseModel):
    factor: str
    value: str | float | None = None
    weight: float | None = None


class MarketSummaryResponseModel(BaseModel):
    market_outlook: str
    confidence: float
    signals: SignalOutputModel
    dominant_factors: list[DominantFactorModel]
    reasoning: str
    risk_level: str
    warnings: list[str]
