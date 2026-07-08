"""
FounderAI backend entrypoint.
Wires up FastAPI, CORS, MongoDB lifecycle events, and all API routers.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    allow_origins=[settings.FRONTEND_ORIGIN],
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


@app.get("/", tags=["health"])
async def root():
    return {"message": "FounderAI API is running. See /docs for API documentation."}
