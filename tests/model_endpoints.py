import structlog

from flare_ai_consensus.router import OpenRouterProvider
from flare_ai_consensus.settings import settings
from flare_ai_consensus.utils import extract_author

logger = structlog.get_logger(__name__)


def get_model_endpoints(provider: OpenRouterProvider, author: str, slug: str) -> None:
    endpoints = provider.get_model_endpoints(author, slug)
    logger.info("model endpoints", endpoints=endpoints)


if __name__ == "__main__":
    # Initialize the OpenRouter provider
    provider = OpenRouterProvider(
        api_key=settings.open_router_api_key,
        base_url=settings.open_router_base_url,
    )
    # Pick a random model_id
    model_id = "qwen/qwen-vl-plus:free"

    author, slug = extract_author(model_id)
    get_model_endpoints(provider, author, slug)
