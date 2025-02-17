from flare_ai_consensus.router import OpenRouterProvider
from flare_ai_consensus.settings import settings
from flare_ai_consensus.utils import save_json


def get_models(provider: OpenRouterProvider) -> dict:
    """List all available models.

    :param provider: the initialized OpenRouterProvider.
    """
    return provider.get_available_models()


def filter_free_models(models_data: dict) -> list:
    """Filter the models that are free.

    :param models_data: json return of provider.get_available_models()
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


if __name__ == "__main__":
    # Initialize the OpenRouter provider
    provider = OpenRouterProvider(
        api_key=settings.open_router_api_key,
        base_url=settings.open_router_base_url,
    )

    # Get all models
    all_models = get_models(provider)
    file_path = settings.data_path / "models.json"

    save_json(all_models, file_path)

    # Get "free" models for additional testing
    free_models = filter_free_models(all_models)
    file_path = settings.data_path / "free_models.json"

    save_json({"data": free_models}, file_path)
