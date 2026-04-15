from pydantic import BaseModel, Field


class MarketSummaryRequest(BaseModel):
    include_news: bool = Field(default=True, description="Include news-derived context in analysis")


class MarketDataModel(BaseModel):
    index: str
    price: float
    change: str
    timestamp: str


class CleanNewsItemModel(BaseModel):
    text: str
    timestamp: str


class SignalOutputModel(BaseModel):
    index: str
    timestamp: str
    trend: str
    momentum: str


class NewsImpactItemModel(BaseModel):
    text: str
    timestamp: str
    sentiment: str
    impact: str
    sector: str


class ContextFactorModel(BaseModel):
    factor: str
    value: str
    contribution: float


class ContextScoresModel(BaseModel):
    signal: float
    news: float
    overall: float


class ContextOutputModel(BaseModel):
    overall_market_sentiment: str
    dominant_factors: list[ContextFactorModel]
    scores: ContextScoresModel
    conflict_detected: bool


class ReasoningOutputModel(BaseModel):
    explanation_text: str
    recommendation: str


class MarketSummaryResponse(BaseModel):
    market_data: MarketDataModel
    cleaned_news: list[CleanNewsItemModel]
    signal_output: SignalOutputModel
    news_impact_output: list[NewsImpactItemModel]
    context_output: ContextOutputModel
    reasoning_output: ReasoningOutputModel
