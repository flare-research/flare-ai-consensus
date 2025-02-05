import json

from src.config import config
from src.router.client import OpenRouterClient

def get_models(client: OpenRouterClient):
    # List available models
    models = client.get_available_models()
    file_path = config.data_path / "models.json"

    with open(file_path, "w") as f:
        json.dump(models, f, indent=4)
    print(f"Models saved to {file_path}.")


def get_model_endpoints(client: OpenRouterClient, author: str, slug: str):
    endpoints = client.get_model_endpoints(author, slug)
    print(endpoints)


if __name__ == "__main__":
    # Initialize the OpenRouter client.
    client = OpenRouterClient(
        api_key=config.open_router_api_key,
        base_url=config.open_router_base_url,
    )

    # Get all models
    get_models(client)
