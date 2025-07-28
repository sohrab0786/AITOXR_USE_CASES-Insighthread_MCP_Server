from fastapi import APIRouter, Query, Request, HTTPException
from typing import Optional, List
from app.services.mcp_tools import (
    get_income_statements, get_balance_sheets, get_cash_flow_statements,
    get_ratios, get_key_metrics, get_price_history, get_latest_price
)
from app.utils.normalize import normalize_metrics

router = APIRouter()

@router.get("/financials/income/{ticker}")
def get_income_statements_api(request: Request, ticker: str, metrics: Optional[List[str]] = Query(default=[]), year: Optional[int] = None, period: Optional[str] = None):
    return get_income_statements(ticker, normalize_metrics(metrics), year, period)

@router.get("/financials/balance/{ticker}")
def get_balance_sheets_api(request: Request, ticker: str, metrics: Optional[List[str]] = Query(default=[]), year: Optional[int] = None, period: Optional[str] = None):
    return get_balance_sheets(ticker, normalize_metrics(metrics), year, period)

@router.get("/financials/cash/{ticker}")
def get_cash_flow_statements_api(request: Request, ticker: str, metrics: Optional[List[str]] = Query(default=[]), year: Optional[int] = None, period: Optional[str] = None):
    return get_cash_flow_statements(ticker, normalize_metrics(metrics), year, period)

@router.get("/ratios/{ticker}")
def get_ratios_api(ticker: str, metrics: Optional[List[str]] = Query(default=[]), year: Optional[int] = None, period: Optional[str] = None):
    return get_ratios(ticker, normalize_metrics(metrics), year, period)

@router.get("/key-metrics/{ticker}")
def get_key_metrics_api(
    ticker: str,
    metrics: Optional[List[str]] = Query(default=[]),
    year: Optional[int] = None,
    period: Optional[str] = None,
):
    print("Raw metrics:", metrics)
    normalized = normalize_metrics(metrics)
    print("Normalized:", normalized)
    return get_key_metrics(ticker, normalized, year, period)

@router.get("/price/history/{ticker}")
def get_price_history_api(ticker: str, year: Optional[int] = None, period: Optional[str] = None):
    return get_price_history(ticker, year, period)

@router.get("/price/{ticker}")
def get_latest_price_api(ticker: str):
    return get_latest_price(ticker)
