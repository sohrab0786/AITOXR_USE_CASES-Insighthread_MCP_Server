from fastapi import HTTPException, Query
from typing import Optional, List
from app.core.supabase_client import fetch_table, supabase
from app.models.schemas import FinancialQuery
"""
def get_income_statements(ticker: str, metrics: Optional[List[str]] = [], year: Optional[int] = None, period: Optional[str] = None):
    rows = fetch_table("financial", "financial_fact", ticker.upper(), metrics, year, period, statement="IS")
    if not rows:
        raise HTTPException(status_code=404, detail="No income statement data found")
    return rows

def get_balance_sheets(ticker: str, metrics: Optional[List[str]] = [], year: Optional[int] = None, period: Optional[str] = None):
    rows = fetch_table("financial", "financial_fact", ticker.upper(), metrics, year, period, statement="BS")
    if not rows:
        raise HTTPException(status_code=404, detail="No balance sheet data found")
    return rows

def get_cash_flow_statements(ticker: str, metrics: Optional[List[str]] = [], year: Optional[int] = None, period: Optional[str] = None):
    rows = fetch_table("financial", "financial_fact", ticker.upper(), metrics, year, period, statement="CF")
    if not rows:
        raise HTTPException(status_code=404, detail="No cash flow statement data found")
    return rows

def get_ratios(ticker: str, metrics: Optional[List[str]] = [], year: Optional[int] = None, period: Optional[str] = None):
    rows = fetch_table("financial", "ratios", ticker.upper(), metrics, year, period)
    if not rows:
        raise HTTPException(status_code=404, detail="No result found")
    return rows

def get_key_metrics(ticker: str, metrics: Optional[List[str]] = [], year: Optional[int] = None, period: Optional[str] = None):
    rows = fetch_table("financial", "key_metrics", ticker.upper(), metrics, year, period)
    if not rows:
        raise HTTPException(status_code=404, detail="No result found")
    return rows

def get_price_history(ticker: str, year: Optional[int] = None, period: Optional[str] = None):
    allowed_periods = {"Q1", "Q2", "Q3", "Q4"}
    if period and period not in allowed_periods:
        raise HTTPException(status_code=400, detail=f"Invalid period: must be one of {allowed_periods}")
    rows = fetch_table("stocks", "eod", ticker.upper(), [], year, period)
    if not rows:
        raise HTTPException(status_code=404, detail="No result found")
    return rows

def get_latest_price(ticker: str):
    response = supabase.schema("refdata").table("companies") \
        .select("symbol, price") \
        .eq("symbol", ticker.upper()) \
        .execute()

    if not response.data:
        raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not found")

    return response.data[0]
"""