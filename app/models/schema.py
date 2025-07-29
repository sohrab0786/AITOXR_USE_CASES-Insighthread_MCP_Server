# fastapi_mcp/app/models/schema.py
from pydantic import BaseModel, validator
from typing import List, Optional

class FinancialParams(BaseModel):
    ticker: str
    metrics: Optional[List[str]] = []
    year: Optional[int] = None
    period: Optional[str] = None

    @validator("period")
    def validate_period(cls, v):
        allowed = {"Q1", "Q2", "Q3", "Q4", "FY"}
        if v and v not in allowed:
            raise ValueError(f"period must be one of {allowed}")
        return v
