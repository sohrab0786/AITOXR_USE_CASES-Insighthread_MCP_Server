import sys
import os
sys.path.insert(0, os.path.abspath("."))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.financial_routes import router as financial_router
#from app.mcp.server.fastmcp import FastMCP  # ✅ FIXED
from app.core.bootstrap import mcp  # ✅ Also correct

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(financial_router)
app.mcp = mcp
