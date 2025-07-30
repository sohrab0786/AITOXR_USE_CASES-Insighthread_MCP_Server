# fastapi_mcp/app/db/supabase_client.py
from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
def fetch_table(
    schema: str,
    table: str,
    ticker: str | dict,
    metrics: list[str] = None,
    year: int | None = None,
    period: str | None = None,
    statement: str | None = None,
    date: str | None = None,
) -> list[dict]:
    assert ticker, "Ticker is required"
    query = supabase.schema(schema).table(table).select("*")

    if isinstance(ticker, dict):
        for key, value in ticker.items():
            query = query.eq(key, value)
    else:
        query = query.eq("ticker", ticker)

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

    elif schema == "financial" and table in ("ratios", "key_metrics"):
        if year:
            query = query.eq("fiscal_year", year)
        if period:
            query = query.eq("fiscal_period", period)
        if metrics:
            query = query.in_("metric", metrics)
        query = query.order("fiscal_year", desc=True).order("fiscal_period", desc=True).limit(50)

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

    elif schema == "congress_trades" and table == "house_trades":
        if year:
            query = query.gte("transaction_date", f"{year}-01-01").lte("transaction_date", f"{year}-12-31")
        if date:
            query = query.eq("transaction_date", date)
        query = query.order("transaction_date", desc=True).limit(100)
        print(f'year: {year}, date: {date}, ticker: {ticker}')
    elif schema =='congress_trades' and table == 'senate_trades':
        if year:
            query = query.gte("transaction_date", f"{year}-01-01").lte("transaction_date", f"{year}-12-31")
        if date:
            query = query.eq("transaction_date", date)
        query = query.order("transaction_date", desc=True).limit(100)
        print(f'year: {year}, date: {date}, ticker: {ticker}')
    elif schema == "insider_trades" and table == "trades":
        if year:
            query = query.gte("transaction_date", f"{year}-01-01").lte("transaction_date", f"{year}-12-31")
        if date:
            query = query.eq("transaction_date", date)
        query = query.order("transaction_date", desc=True).limit(100)
    elif schema == "filings" and table == "filings":
        if year:
            query = query.gte("filing_date", f"{year}-01-01").lte("filing_date", f"{year}-12-31")
        if date:
            query = query.gte("filing_date", f"{date}").lt("filing_date", f"{date}T23:59:59")
        query = query.order("filing_date", desc=True).limit(100)
    elif schema == "news" and table == "articles":
        if year:
            query = query.gte("published_date", f"{year}-01-01").lte("published_date", f"{year}-12-31")
        if date:
            # Capture whole day: from 00:00 to 23:59:59
            query = query.gte("published_date", f"{date}T00:00:00").lte("published_date", f"{date}T23:59:59")
        query = query.order("published_date", desc=True).limit(100)
    else:
        query = query.limit(50)

    resp = query.execute()
    return resp.data or []
