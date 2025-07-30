# fastapi_mcp/app/api/routes.py
from fastapi import APIRouter, Query, HTTPException, Request
from typing import List, Optional
from app.services.mcp_handler import (
    get_income_statements,
    get_balance_sheets,
    get_cash_flow_statements,
    get_ratios,
    get_key_metrics,
    get_price_history,
    get_latest_price,
    normalize_metrics,
    ping,
    get_congress_trades_house,
    get_congress_trades_senate,
    get_insider_trades,
    get_filings,
    get_news_articles
)

router = APIRouter()

@router.get("/mcp/ping-test")
def test_mcp_tool():
    return ping()

@router.get("/financials/income/{ticker}")
def get_income_statements_api(ticker: str, metrics: Optional[List[str]] = Query(default=[]), year: Optional[int] = None, period: Optional[str] = None):
    return get_income_statements(ticker, normalize_metrics(metrics), year, period)

@router.get("/financials/balance/{ticker}")
def get_balance_sheets_api(ticker: str, metrics: Optional[List[str]] = Query(default=[]), year: Optional[int] = None, period: Optional[str] = None):
    return get_balance_sheets(ticker, normalize_metrics(metrics), year, period)

@router.get("/financials/cash/{ticker}")
def get_cash_flow_statements_api(ticker: str, metrics: Optional[List[str]] = Query(default=[]), year: Optional[int] = None, period: Optional[str] = None):
    return get_cash_flow_statements(ticker, normalize_metrics(metrics), year, period)

@router.get("/ratios/{ticker}")
def get_ratios_api(ticker: str, metrics: Optional[List[str]] = Query(default=[]), year: Optional[int] = None, period: Optional[str] = None):
    return get_ratios(ticker, normalize_metrics(metrics), year, period)

@router.get("/key-metrics/{ticker}")
def get_key_metrics_api(ticker: str, metrics: Optional[List[str]] = Query(default=[]), year: Optional[int] = None, period: Optional[str] = None):
    return get_key_metrics(ticker, normalize_metrics(metrics), year, period)

@router.get("/price/history/{ticker}")
def get_price_history_api(ticker: str, year: Optional[int] = None, period: Optional[str] = None):
    return get_price_history(ticker, year, period)

@router.get("/price/{ticker}")
def get_latest_price_api(ticker: str):
    return get_latest_price(ticker)

@router.get("/congress-trades/house_trades")
def congress_trades_api(
    symbol: str = Query(..., description="Ticker symbol (required)"),
    year: int = None,
    date: str = None,
):
    return get_congress_trades_house(symbol, year, date)
@router.get("/congress-trades/senate_trades")
def senate_trades_api(
    symbol: str = Query(..., description="Ticker symbol (required)"),
    year: int = None,
    date: str = None,
):
    return get_congress_trades_senate(symbol, year, date)
@router.get("/insider-trades")
def insider_trades_api(
    symbol: str = Query(..., description="Ticker symbol (required)"),
    year: int = None,
    date: str = None,
):
    return get_insider_trades(symbol, year, date)
@router.get("/filings")
def filings_api(
    symbol: str = Query(..., description="Ticker symbol (required)"),
    year: Optional[int] = None,
    date: Optional[str] = None,
):
    return get_filings(symbol, year, date)

@router.get("/news")
def news_api(
    symbol: str = Query(..., description="Ticker symbol (required)"),
    category: Optional[str] = None,
    year: Optional[int] = None,
    date: Optional[str] = None,
):
    return get_news_articles(symbol, category, year, date)
