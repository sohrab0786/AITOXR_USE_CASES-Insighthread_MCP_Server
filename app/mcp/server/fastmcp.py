# mcp/server/fastmcp.py
import os
import sys
from typing import List, Optional

from app.core.supabase_client import fetch_table
from fastapi import HTTPException
# mcp/server/fastmcp.py

class FastMCP:
    def __init__(self, datasource: str):
        self.datasource = datasource

    def _check_source(self):
        if self.datasource != "supabase-financial":
            raise NotImplementedError("Only 'supabase-financial' is supported currently.")

    def get_income_statements(self, ticker: str, metrics: Optional[List[str]] = [], year: Optional[int] = None, period: Optional[str] = None):
        rows = fetch_table("financial", "financial_fact", ticker.upper(), metrics, year, period, statement="IS")
        if not rows:
            raise HTTPException(status_code=404, detail="No income statement data found")
        return rows

    def get_balance_sheets(self, ticker: str, metrics: Optional[List[str]] = [], year: Optional[int] = None, period: Optional[str] = None):
        rows = fetch_table("financial", "financial_fact", ticker.upper(), metrics, year, period, statement="BS")
        if not rows:
            raise HTTPException(status_code=404, detail="No balance sheet data found")
        return rows

    def get_cash_flow_statements(self, ticker: str, metrics: Optional[List[str]] = [], year: Optional[int] = None, period: Optional[str] = None):
        rows = fetch_table("financial", "financial_fact", ticker.upper(), metrics, year, period, statement="CF")
        if not rows:
            raise HTTPException(status_code=404, detail="No cash flow statement data found")
        return rows


    def get_ratios(self, ticker: str, metrics: List[str], year=None, period=None):
        self._check_source()
        return fetch_table("financial", "ratios", ticker, metrics, year, period)

    def get_key_metrics(self, ticker: str, metrics: List[str], year=None, period=None):
        self._check_source()
        return fetch_table("financial", "key_metrics", ticker, metrics, year, period)

    def get_stock_prices(self, ticker: str, year=None, period=None):
        self._check_source()
        return fetch_table("stocks", "eod", ticker, year=year, period=period)

    def get_latest_price(self, ticker: str):
        self._check_source()
        return fetch_table("refdata", "companies", {"symbol": ticker})
