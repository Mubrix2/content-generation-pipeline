# app/api/routes/generate.py
import logging
from fastapi import APIRouter, HTTPException, status
from app.api.schemas import (
    GenerateRequest,
    GenerateResponse,
    CaptionsOutput,
    EmailOutput,
    ToneOption,
    TonesResponse,
)
from app.services.pipeline import run_pipeline

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/generate", tags=["Generate"])

TONES = [
    ToneOption(value="professional", description="Formal and authoritative"),
    ToneOption(value="casual", description="Friendly and conversational"),
    ToneOption(value="inspirational", description="Motivating and uplifting"),
    ToneOption(value="educational", description="Clear and informative"),
]


@router.get(
    "/tones",
    response_model=TonesResponse,
    summary="List available writing tones",
)
async def list_tones():
    """Return all supported tone options for content generation."""
    return TonesResponse(tones=TONES)


@router.post(
    "",
    response_model=GenerateResponse,
    summary="Generate a full content package from a topic",
)
async def generate_content(request: GenerateRequest):
    """
    Run the full content pipeline:
    topic → outline → blog post → summary → captions + email.

    Takes 15-25 seconds as it makes five sequential LLM calls.
    """
    try:
        result = run_pipeline(
            topic=request.topic,
            tone=request.tone,
            audience=request.audience,
        )

        return GenerateResponse(
            topic=result["topic"],
            tone=result["tone"],
            audience=result["audience"],
            outline=result["outline"],
            blog_post=result["blog_post"],
            summary=result["summary"],
            captions=CaptionsOutput(**result["captions"]),
            email=EmailOutput(**result["email"]),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Content generation failed. Please try again.",
        )