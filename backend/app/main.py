"""
FounderAI backend entrypoint.
Wires up FastAPI, CORS, MongoDB lifecycle events, and all API routers.
"""
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes import auth, generate, profile
from app.core.config import settings
from app.db.mongo import close_mongo_connection, connect_to_mongo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("founderai")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting FounderAI backend (env=%s)...", settings.APP_ENV)
    await connect_to_mongo()
    yield
    await close_mongo_connection()
    logger.info("FounderAI backend shut down cleanly.")


app = FastAPI(
    title="FounderAI API",
    description="Multi-Agent AI Startup Builder — turns a startup idea into a full business blueprint.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(generate.router)


@app.get("/health", tags=["health"])
async def health_check():
    """Simple liveness check used by Render and uptime monitors."""
    return {"status": "ok", "service": "founderai-backend"}


# Mount static files and serve frontend
STATIC_DIR = Path(__file__).parent.parent.parent / "frontend" / "dist"
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend for all non-API routes."""
        # Skip API routes
        if full_path.startswith("api/") or full_path.startswith("health") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return {"message": "API route not found"}
        
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        # For SPA routing, return index.html
        return FileResponse(STATIC_DIR / "index.html")
else:
    @app.get("/", tags=["health"])
    async def root():
        return {"message": "FounderAI API is running. See /docs for API documentation."}
