import structlog
import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from flare_ai_consensus.api import ChatRouter
from flare_ai_consensus.router import AsyncOpenRouterProvider
from flare_ai_consensus.settings import settings
from flare_ai_consensus.utils import load_json

logger = structlog.get_logger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    This function:
      1. Creates a new FastAPI instance with optional CORS middleware.
      2. Loads configuration.
      3. Sets up the OpenRouter client.
      4. Initializes a ChatRouter that wraps the RAG pipeline.
      5. Registers the chat endpoint under the /chat prefix.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(
        title="Flare AI Consensus Learning", version="1.0", redirect_slashes=False
    )

    # Optional: configure CORS middleware using settings.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Load input configuration.
    config_json = load_json(settings.input_path / "input.json")
    settings.load_consensus_config(config_json)

    # Initialize the OpenRouter provider.
    provider = AsyncOpenRouterProvider(
        api_key=settings.open_router_api_key, base_url=settings.open_router_base_url
    )

    # Create an APIRouter for chat endpoints and initialize ChatRouter.
    chat_router = ChatRouter(
        router=APIRouter(),
        provider=provider,
        consensus_config=settings.consensus_config,
    )
    app.include_router(chat_router.router, prefix="/api/routes/chat", tags=["chat"])

    return app


app = create_app()


def start() -> None:
    """
    Start the FastAPI application server.
    """
    uvicorn.run(app, host="0.0.0.0", port=80)  # noqa: S104


if __name__ == "__main__":
    start()
