import os
import uvicorn
from fastapi import FastAPI
from core.sqlite_db import SQLiteDB
from fastapi.middleware.cors import CORSMiddleware
from services import category_service, inventory_service, user_service
from routers import users, categories, inventory


from google.adk.cli.fast_api import get_fast_api_app
from fastapi.staticfiles import StaticFiles

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔧 Fix for Pydantic v2 schema generation error with MCP ClientSession
try:
    import mcp.client.session
    from pydantic_core import core_schema
    mcp.client.session.ClientSession.__get_pydantic_core_schema__ = classmethod(
        lambda cls, source_type, handler: core_schema.any_schema()
    )
except ImportError:
    pass

# Configure allowed origins for CORS
ALLOWED_ORIGINS = ["*"]

# Initialize the ADK app
# agents_dir should be the directory containing agent folders
app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=False,
    allow_origins=ALLOWED_ORIGINS
)

# Include custom routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])

# Serve frontend static files
frontend_dir = os.path.abspath(os.path.join(AGENT_DIR, "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
