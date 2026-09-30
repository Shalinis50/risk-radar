from typing import List
from pydantic import BaseModel


class TransactionCreate(BaseModel):
    user_id: str
    amount: float
    timestamp: str
    latitude: float
    longitude: float


class TransactionResponse(BaseModel):
    id: int
    user_id: str
    amount: float
    timestamp: str
    latitude: float
    longitude: float
    risk_score: int
    risk_level: str
    flagged: bool
    triggered_rules: List[str]
    review_status: str


class ReviewUpdate(BaseModel):
    review_status: str