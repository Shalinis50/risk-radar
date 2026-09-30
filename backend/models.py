from typing import Optional
from sqlmodel import SQLModel, Field


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: str
    amount: float
    timestamp: str
    latitude: float
    longitude: float

    risk_score: int = 0
    risk_level: str = "LOW"
    flagged: bool = False
    triggered_rules: str = ""
    review_status: str = "PENDING"