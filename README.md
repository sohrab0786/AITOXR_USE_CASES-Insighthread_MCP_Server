
This project uses mcp to query via url and get responses from supabase DB

**Steps**
1. git clone https://github.com/sohrab0786/AITOXR_USE_CASES-Insighthread_MCP_Server.git
2. cd AITOXR_USE_CASES-Insighthread_MCP_Server
3. then install uv see steps on chatgpt.
4. create virtual environment using uv 
5. install pyproject.toml requirements using uv 
   uv pip install -r pyproject.toml
6. insert required details in .env file

Finally Run it like this 
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000          
then search in browser 
e.g http://127.0.0.1:8000/financials/income/AAPL?year=2022&period=Q2&metrics=netIncome,revenue

http://127.0.0.1:8000/financials/balance/AAPL?year=2022&period=Q2

http://127.0.0.1:8000/financials/cash/AAPL?year=2022&period=Q2

