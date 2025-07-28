from fastapi import APIRouter, Query, Request, HTTPException
from typing import Optional, List
#from app.services.mcp_tools import (
#    get_income_statements, get_balance_sheets, get_cash_flow_statements,
#    get_ratios, get_key_metrics, get_price_history, get_latest_price
#)
from app.utils.normalize import normalize_metrics

router = APIRouter()
# app/routes/financial_routes.py
from fastapi import APIRouter, Query, Request
from app.mcp.server.fastmcp import FastMCP
from app.utils.normalize import normalize_metrics

router = APIRouter()
mcp = FastMCP("supabase-financial")

@router.get("/financials/income/{ticker}")
def get_income_statements(ticker: str, metrics: List[str] = Query([]), year: int = None, period: str = None):
    return mcp.get_income_statements(ticker, normalize_metrics(metrics), year, period)

@router.get("/financials/balance/{ticker}")
def get_balance_sheets(ticker: str, metrics: List[str] = Query([]), year: int = None, period: str = None):
    return mcp.get_balance_sheets(ticker, normalize_metrics(metrics), year, period)

@router.get("/financials/cash/{ticker}")
def get_cash_flow_statements(ticker: str, metrics: List[str] = Query([]), year: int = None, period: str = None):
    return mcp.get_cash_flow_statements(ticker, normalize_metrics(metrics), year, period)

@router.get("/ratios/{ticker}")
def get_ratios(ticker: str, metrics: List[str] = Query([]), year: int = None, period: str = None):
    return mcp.get_ratios(ticker, normalize_metrics(metrics), year, period)

@router.get("/key-metrics/{ticker}")
def get_key_metrics(ticker: str, metrics: List[str] = Query([]), year: int = None, period: str = None):
    return mcp.get_key_metrics(ticker, normalize_metrics(metrics), year, period)

@router.get("/price/history/{ticker}")
def get_price_history(ticker: str, year: int = None, period: str = None):
    return mcp.get_stock_prices(ticker, year, period)

@router.get("/price/{ticker}")
def get_latest_price(ticker: str):
    return mcp.get_latest_price(ticker)
