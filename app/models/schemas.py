from pydantic import BaseModel, validator
from typing import List, Optional

class FinancialQuery(BaseModel):
    ticker: str
    metrics: Optional[List[str]] = []
    year: Optional[int] = None
    period: Optional[str] = None

    @validator("period")
    def check_period(cls, v):
        if v and v not in {"Q1", "Q2", "Q3", "Q4", "FY"}:
            raise ValueError("Period must be Q1, Q2, Q3, Q4 or FY")
        return v
