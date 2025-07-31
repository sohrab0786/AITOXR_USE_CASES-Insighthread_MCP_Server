# fastapi_mcp/app/services/mcp_handler.py
from fastapi import HTTPException, Query
from typing import List, Optional, Union
from mcp.server.fastmcp import FastMCP
from app.db.supabase_client import fetch_table, supabase
from app.models.schema import FinancialParams

mcp = FastMCP("supabase-financial")

def normalize_metrics(metrics: Optional[Union[List[str], str]]) -> List[str]:
    if not metrics:
        return []
    if isinstance(metrics, str):
        return [m.strip() for m in metrics.split(",")]
    if isinstance(metrics, list) and len(metrics) == 1 and "," in metrics[0]:
        return [m.strip() for m in metrics[0].split(",")]
    return [m.strip() for m in metrics if isinstance(m, str)]

@mcp.tool()
def ping() -> dict:
    return {"status": "MCP is active"}

@mcp.tool()
def get_income_statements(ticker: str, metrics: List[str] = [], year: Optional[int] = None, period: Optional[str] = None):
    params = FinancialParams(ticker=ticker.upper(), metrics=metrics, year=year, period=period)
    rows = fetch_table("financial", "financial_fact", params.ticker, params.metrics, params.year, params.period, statement="IS")
    if not rows:
        raise HTTPException(status_code=404, detail="No income statement data found")
    return rows
@mcp.tool()
def get_balance_sheets(ticker: str, metrics: List[str] = [], year: Optional[int] = None, period: Optional[str] = None):
    params = FinancialParams(ticker=ticker.upper(), metrics=metrics, year=year, period=period)
    rows = fetch_table("financial", "financial_fact", params.ticker, params.metrics, params.year, params.period, statement="BS")
    if not rows:
        raise HTTPException(status_code=404, detail="No balance sheet data found")
    return rows
@mcp.tool()
def get_cash_flow_statements(ticker: str, metrics: List[str] = [], year: Optional[int] = None, period: Optional[str] = None):
    params = FinancialParams(ticker=ticker.upper(), metrics=metrics, year=year, period=period)
    rows = fetch_table("financial", "financial_fact", params.ticker, params.metrics, params.year, params.period, statement="CF")
    if not rows:
        raise HTTPException(status_code=404, detail="No cash flow statement data found")
    return rows
@mcp.tool()
def get_ratios(ticker: str, metrics: List[str] = [], year: Optional[int] = None, period: Optional[str] = None):
    params = FinancialParams(ticker=ticker.upper(), metrics=metrics, year=year, period=period)
    rows = fetch_table("financial", "ratios", params.ticker, params.metrics, params.year, params.period)
    if not rows:
        raise HTTPException(status_code=404, detail="No ratios data found")
    return rows
@mcp.tool()
def get_key_metrics(ticker: str, metrics: List[str] = [], year: Optional[int] = None, period: Optional[str] = None):
    params = FinancialParams(ticker=ticker.upper(), metrics=metrics, year=year, period=period)
    rows = fetch_table("financial", "key_metrics", params.ticker, params.metrics, params.year, params.period)
    if not rows:
        raise HTTPException(status_code=404, detail="No key metrics data found")
    return rows
@mcp.tool()
def get_price_history(ticker: str, year: Optional[int] = None, period: Optional[str] = None):
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker is required")
    rows = fetch_table("stocks", "eod", ticker.upper(), year=year, period=period)
    if not rows:
        raise HTTPException(status_code=404, detail="No price history data found")
    return rows

@mcp.tool()
def get_latest_price(ticker: str):
    rows = fetch_table("refdata", "companies", {"symbol": ticker.upper()})
    if not rows:
        raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not found")
    return rows[0]
@mcp.tool()
def get_congress_trades_house(symbol: str, year: int = None, date: str = None):
    filters = {"symbol": symbol.upper()}

    rows = fetch_table("congress_trades", "house_trades", ticker=filters, year=year, date=date)
    if not rows:
        raise HTTPException(status_code=404, detail="No congress trades data found")
    return rows
@mcp.tool()
def get_congress_trades_senate(symbol: str, year: int = None, date: str = None):
    filters = {"symbol": symbol.upper()}

    rows = fetch_table("congress_trades", "senate_trades", ticker=filters, year=year, date=date)
    if not rows:
        raise HTTPException(status_code=404, detail="No congress trades data found")
    return rows

@mcp.tool()
def get_insider_trades(symbol: str, year: int = None, date: str = None):
    if not symbol:
        raise HTTPException(status_code=400, detail="Symbol is required")
    filters = {"symbol": symbol.upper()}
    rows = fetch_table("insider_trades", "trades", ticker=filters, year=year, period=None, statement=None, date=date)
    if not rows:
        raise HTTPException(status_code=404, detail="No insider trades data found")
    return rows

@mcp.tool()
def get_filings(symbol: str, year: Optional[int] = None, date: Optional[str] = None):
    if not symbol:
        raise HTTPException(status_code=400, detail="Symbol is required")

    filters = {"symbol": symbol.upper()}
    rows = fetch_table("filings", "filings", ticker=filters, year=year, date=date)
    if not rows:
        raise HTTPException(status_code=404, detail="No filings data found")
    return rows

@mcp.tool()
def get_news_articles(symbol: str, category: str = None, year: int = None, date: str = None):
    symbol = symbol.upper()

    # If no category, fetch directly from articles
    if not category:
        return fetch_table("news", "articles", ticker={"symbol": symbol}, year=year, date=date)

    # Step 1: Get category ID
    category_resp = supabase.schema("news").table("categories").select("id").eq("name", category.lower()).execute()
    if not category_resp.data:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
    category_id = category_resp.data[0]["id"]

    # Step 2: Get article IDs from article_categories
    filters = {"symbol": symbol, "category_id": category_id}
    article_refs = fetch_table("news", "article_categories", ticker=filters, year=year, date=date)

    if not article_refs:
        raise HTTPException(status_code=404, detail="No articles found for given filters")

    # Step 3: Fetch matching articles (only needed fields to avoid timeout)
    article_ids = [ref["article_id"] for ref in article_refs]
    if not article_ids:
        raise HTTPException(status_code=404, detail="No matching articles found")

    # Split into batches if needed to avoid Supabase URL limits
    def chunk(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    articles = []
    for id_batch in chunk(article_ids, 50):  # Supabase URL limits
        resp = supabase.schema("news").table("articles")\
            .select("id, symbol, published_date, title, content, url")\
            .in_("id", id_batch)\
            .order("published_date", desc=True)\
            .limit(100)\
            .execute()
        articles.extend(resp.data or [])

    return articles
