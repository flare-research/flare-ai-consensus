from src.router.base_client import BaseClient


class OpenRouterClient(BaseClient):
    """Client to interact with the OpenRouter API."""

    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        """Initialize the OpenRouter client."""

        super().__init__(base_url, api_key)

    def get_available_models(self) -> dict:
        """
        List available models.
        
        API Reference: https://openrouter.ai/docs/api-reference/list-available-models
        :return: A dictionary containing the list of available models.
        """
        endpoint = "/models"
        return self._get(endpoint)

    def get_model_endpoints(self, author: str, slug: str) -> dict:
        """List endpoints for a specific model.
        
        API Reference: https://openrouter.ai/docs/api-reference/list-endpoints-for-a-model
        :param author: The model author.
        :param slug: The model slug.
        :return: A dictionary containing the endpoints for the specified model.
        """
        endpoint = f"/models/{author}/{slug}/endpoints"
        return self._get(endpoint)

    def get_credits(self) -> dict:
        """
        Retrieve the available credits.
        
        API Reference: https://openrouter.ai/docs/api-reference/credits
        :return: A dictionary containing the credits information.
        """
        endpoint = "/credits"
        return self._get(endpoint)
