from src.config import config
from src.router.client import OpenRouterClient
from src.utils.openrouter import extract_author


def get_model_endpoints(client: OpenRouterClient, author: str, slug: str):
    endpoints = client.get_model_endpoints(author, slug)
    print(endpoints)


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
