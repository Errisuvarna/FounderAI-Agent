"""
Generate route: POST /generate.
Creates a startup record, runs the 5-agent CrewAI pipeline (offloaded to a
threadpool since CrewAI's kickoff is a blocking call), persists the
resulting blueprint, and returns it to the client.
"""
import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.agents.crew_orchestrator import run_startup_crew
from app.api.deps import get_current_user
from app.db.mongo import get_db
from app.models.startup import BlueprintResponse, GenerateBlueprintRequest
from app.repositories.startup_repo import (
    create_startup,
    save_blueprint,
    serialize_blueprint,
    update_startup_status,
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["generate"])


@router.post("/generate", response_model=BlueprintResponse, status_code=status.HTTP_201_CREATED)
async def generate_blueprint(
    payload: GenerateBlueprintRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """
    Run the full multi-agent CrewAI pipeline for a startup idea and return
    the generated business blueprint (market research, financials, tech
    architecture, growth strategy, and pitch deck outline).
    """
    user_id = str(current_user["_id"])

    startup = await create_startup(
        db,
        user_id=user_id,
        idea_title=payload.idea_title,
        idea_description=payload.idea_description,
        industry=payload.industry,
        target_market=payload.target_market,
    )
    startup_id = str(startup["_id"])

    await update_startup_status(db, startup_id, "running")

    try:
        # CrewAI's kickoff() is synchronous/blocking, so run it off the event loop.
        blueprint_data = await run_in_threadpool(
            run_startup_crew,
            startup_id,
            payload.idea_title,
            payload.idea_description,
            payload.industry,
            payload.target_market,
        )
    except Exception as exc:
        logger.exception("Crew execution failed for startup_id=%s", startup_id)
        await update_startup_status(db, startup_id, "failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Blueprint generation failed: {exc}",
        ) from exc

    saved = await save_blueprint(db, startup_id, blueprint_data)
    await update_startup_status(db, startup_id, "completed")

    return serialize_blueprint(saved)
