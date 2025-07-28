from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
def fetch_table(
    schema: str,
    table: str,
    ticker: str,
    metrics: list[str] = None,
    year: int | None = None,
    period: str | None = None,
    statement: str | None = None,
) -> list[dict]:
    assert ticker, "Ticker is required"
    query = supabase.schema(schema).table(table).select("*").eq("ticker", ticker)
    # financial_fact (income, balance, cashflow)
    if schema == "financial" and table == "financial_fact":
        if statement:
            query = query.eq("statement", statement)
        if year:
            query = query.eq("fiscal_year", year)
        if period:
            query = query.eq("fiscal_period", period)
        if metrics:
            query = query.in_("metric", metrics)
        query = query.order("fiscal_year", desc=True).order("fiscal_period", desc=True).limit(50)
    # ratios and key_metrics filtering
    elif schema == "financial" and table in ("ratios", "key_metrics"):
        if year:
            query = query.eq("fiscal_year", year)
        if period:
            query = query.eq("fiscal_period", period)
        if metrics:
            query = query.in_("metric", metrics)
        query = query.order("fiscal_year", desc=True).order("fiscal_period", desc=True).limit(50)
    # historical prices
    elif schema == "stocks" and table == "eod":
        if year or period:
            quarters = {
                "Q1": (f"{year}-01-01", f"{year}-03-31"),
                "Q2": (f"{year}-04-01", f"{year}-06-30"),
                "Q3": (f"{year}-07-01", f"{year}-09-30"),
                "Q4": (f"{year}-10-01", f"{year}-12-31"),
            }
            if year and period and period in quarters:
                start, end = quarters[period]
                query = query.gte("date", start).lte("date", end)
            elif year:
                query = query.gte("date", f"{year}-01-01").lte("date", f"{year}-12-31")
        query = query.order("date", desc=True).limit(200)
    else:
        # fallback
        query = query.limit(50)
    resp = query.execute()
    return resp.data or []
