# mcp/server/fastmcp.py
import os
import sys
from typing import List, Optional

from app.core.supabase_client import fetch_table

class FastMCP:
    def __init__(self, datasource: str):
        self.datasource = datasource

    def get_financial_data(
        self,
        ticker: str,
        metrics: List[str],
        year: Optional[int] = None,
        period: Optional[str] = None,
        statement: Optional[str] = None,
    ) -> List[dict]:
        """
        Fetch financial facts from Supabase.
        """
        if self.datasource != "supabase-financial":
            raise NotImplementedError("Only 'supabase-financial' is supported currently.")
        
        return fetch_table(
            schema="financial",
            table="financial_fact",
            ticker=ticker,
            metrics=metrics,
            year=year,
            period=period,
            statement=statement,
        )

    def get_stock_prices(
        self,
        ticker: str,
        year: Optional[int] = None,
        period: Optional[str] = None
    ) -> List[dict]:
        """
        Fetch EOD stock prices from Supabase.
        """
        return fetch_table(
            schema="stocks",
            table="eod",
            ticker=ticker,
            year=year,
            period=period
        )
