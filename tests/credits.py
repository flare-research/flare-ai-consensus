import structlog

from flare_ai_consensus.router import OpenRouterProvider
from flare_ai_consensus.settings import settings

logger = structlog.get_logger(__name__)


def get_credits(provider: OpenRouterProvider) -> None:
    # Retrieve available credits
    current_credits = provider.get_credits()
    logger.info("current credits", current_credits=current_credits)


if __name__ == "__main__":
    # Initialize the OpenRouter provider.
    provider = OpenRouterProvider(
        api_key=settings.open_router_api_key,
        base_url=settings.open_router_base_url,
    )

    get_credits(provider)
