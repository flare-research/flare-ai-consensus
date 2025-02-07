from src.router.base_client import AsyncBaseClient


class AsyncOpenRouterClient(AsyncBaseClient):
    """Asynchronous client to interact with the OpenRouter API."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        """
        Initialize the AsyncOpenRouterClient.

        :param api_key: Optional API key for authentication.
        :param base_url: Optional custom base URL.
        """
        if base_url is None:
            base_url = "https://openrouter.ai/api/v1"
        super().__init__(base_url, api_key)

    async def send_completion(self, payload: dict) -> dict:
        """
        Send a prompt to the completions endpoint.

        :param payload: The JSON payload.
        :return: The JSON response from the API.
        """
        endpoint = "/completions"
        return await self._post(endpoint, payload)

    async def send_chat_completion(self, payload: dict) -> dict:
        """
        Send a prompt to the chat completions endpoint.

        :param payload: The JSON payload.
        :return: The JSON response from the API.
        """
        endpoint = "/chat/completions"
        return await self._post(endpoint, payload)
