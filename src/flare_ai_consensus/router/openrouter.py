from flare_ai_consensus.router.base_router import (
    AsyncBaseRouter,
    BaseRouter,
    ChatRequest,
    CompletionRequest,
)


class OpenRouterProvider(BaseRouter):
    """Sync provider to interact with the OpenRouter API."""

    def __init__(
        self, api_key: str | None = None, base_url: str = "https://openrouter.ai/api/v1"
    ) -> None:
        """
        Initialize the OpenRouter provider.

        The base URL is set to the OpenRouter API endpoint by default,
        but can be overridden.
        :param api_key: Optional API key for authentication.
        :param base_url: Optional custom base URL.
            Defaults to "https://openrouter.ai/api/v1"
        """
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
        """
        List endpoints for a specific model.

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

    def send_completion(self, payload: CompletionRequest) -> dict:
        """
        Send a prompt to the completions endpoint.

        The completions endpoint expects a JSON payload with keys
        like "model" and "prompt".
        """
        endpoint = "/completions"
        return self._post(endpoint, payload)

    def send_chat_completion(self, payload: ChatRequest) -> dict:
        """
        Send a prompt to the chat completions endpoint.

        The payload should include a "model" field and a "messages"
        array where each message has a "role"
        (e.g., "user", "assistant", "system") and "content".
        """
        endpoint = "/chat/completions"
        return self._post(endpoint, payload)


class AsyncOpenRouterProvider(AsyncBaseRouter):
    """Asynchronous provider to interact with the OpenRouter API."""

    def __init__(
        self, api_key: str | None = None, base_url: str = "https://openrouter.ai/api/v1"
    ) -> None:
        """
        Initialize the AsyncOpenRouterProvider.

        :param api_key: Optional API key for authentication.
        :param base_url: Optional custom base URL.
        """
        super().__init__(base_url, api_key)

    async def send_completion(self, payload: CompletionRequest) -> dict:
        """
        Send a prompt to the completions endpoint.

        :param payload: The JSON payload.
        :return: The JSON response from the API.
        """
        endpoint = "/completions"
        return await self._post(endpoint, payload)

    async def send_chat_completion(self, payload: ChatRequest) -> dict:
        """
        Send a prompt to the chat completions endpoint.

        :param payload: The JSON payload.
        :return: The JSON response from the API.
        """
        endpoint = "/chat/completions"
        return await self._post(endpoint, payload)
