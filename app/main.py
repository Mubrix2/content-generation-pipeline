# app/main.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import generate, health
from app.config import APP_ENV
from app.core.generator import get_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting Content Generation Pipeline | env={APP_ENV}")
    get_client()
    logger.info("Groq client ready.")
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Content Generation Pipeline",
        description=(
            "Generate blog posts, social captions, and email copy "
            "from a single topic using a prompt chaining pipeline."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(generate.router, prefix="/api/v1")

    return app


app = create_app()