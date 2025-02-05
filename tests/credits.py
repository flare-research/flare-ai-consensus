from src.config import config
from src.router.client import OpenRouterClient


def get_credits(client: OpenRouterClient) -> None:
    # Retrieve available credits
    current_credits = client.get_credits()
    print(current_credits)


if __name__ == "__main__":
    # Initialize the OpenRouter client.
    client = OpenRouterClient(
        api_key=config.open_router_api_key,
        base_url=config.open_router_base_url,
    )

    get_credits(client)
