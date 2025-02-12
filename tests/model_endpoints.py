import structlog

from flare_ai_consensus.config import config
from flare_ai_consensus.router.client import OpenRouterClient
from flare_ai_consensus.utils.openrouter import extract_author

logger = structlog.get_logger(__name__)


def get_model_endpoints(client: OpenRouterClient, author: str, slug: str) -> None:
    endpoints = client.get_model_endpoints(author, slug)
    logger.info("model endpoints", endpoints=endpoints)


if __name__ == "__main__":
    # Initialize the OpenRouter client.
    client = OpenRouterClient(
        api_key=config.open_router_api_key,
        base_url=config.open_router_base_url,
    )
    # Pick a random model_id
    model_id = "qwen/qwen-vl-plus:free"

    author, slug = extract_author(model_id)
    get_model_endpoints(client, author, slug)
