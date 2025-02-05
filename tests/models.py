import json
from pathlib import Path

from src.config import config
from src.router.client import OpenRouterClient

def get_models(client: OpenRouterClient) -> dict:
    """List all available models.

    :param client: the initialized OpenRouterClient.
    """
    return client.get_available_models()


def filter_free_models(models_data: dict) -> list:
    """Filter the models that are free.

    :param models_data: json return of client.get_available_models()
    :return: A json of models that meet the free criteria.
    """
    free_models = []
    models = models_data.get("data", [])

    for model in models:
        pricing = model.get("pricing", {})

        # Check if pricing values are all "0"
        free_pricing = all(str(price).strip() == "0" for price in pricing.values())

        if free_pricing:
            free_models.append(model)

    return free_models

def save_json(contents: dict, file_path: Path) -> None:
    with open(file_path, "w") as f:
        json.dump(contents, f, indent=4)
    print(f"Data saved to {file_path}.")


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
    all_models = get_models(client)
    file_path = config.data_path / "models.json"

    save_json(all_models, file_path)

    # Get "free" models for additional testing
    free_models = filter_free_models(all_models)
    file_path = config.data_path / "free_models.json"

    save_json({"data": free_models}, file_path)
