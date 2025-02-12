import structlog

from flare_ai_consensus.config import config
from flare_ai_consensus.router.client import OpenRouterClient

logger = structlog.get_logger(__name__)


def get_credits(client: OpenRouterClient) -> None:
    # Retrieve available credits
    current_credits = client.get_credits()
    logger.info("current credits", current_credits=current_credits)


if __name__ == "__main__":
    # Initialize the OpenRouter client.
    client = OpenRouterClient(
        api_key=config.open_router_api_key,
        base_url=config.open_router_base_url,
    )

    get_credits(client)
