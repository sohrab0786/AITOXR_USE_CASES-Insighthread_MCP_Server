# fastapi_mcp/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.services.mcp_handler import mcp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
def on_startup():
    print("Starting Supabase-backed MCP Server...")

if __name__ == "__main__":
    mcp.run(transport="stdio")
    print("Server stopped")
