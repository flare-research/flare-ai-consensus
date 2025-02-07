import httpx


class AsyncBaseClient:
    """An asynchronous base class to handle HTTP requests and common logic for API interaction."""

    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        """
        :param base_url: The base URL for the API.
        :param api_key: Optional API key for authentication.
        """
        self.base_url = base_url.rstrip("/")  # Ensure no trailing slash
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30.0)
        self.headers = {"accept": "application/json"}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    async def _get(self, endpoint: str, params: dict | None = None) -> dict:
        """
        Make an asynchronous GET request to the API and return the JSON response.

        :param endpoint: The API endpoint (should begin with a slash, e.g., "/models").
        :param params: Optional query parameters.
        :return: JSON response as a dictionary.
        """
        params = params or {}
        url = self.base_url + endpoint
        response = await self.client.get(url, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            msg = f"Error ({response.status_code}): {response.text}"
            raise ConnectionError(msg)

    async def _post(self, endpoint: str, json_payload: dict) -> dict:
        """
        Make an asynchronous POST request to the API with a JSON payload and return the JSON response.

        :param endpoint: The API endpoint (should begin with a slash, e.g., "/completions").
        :param json_payload: The JSON payload to send.
        :return: JSON response as a dictionary.
        """
        url = self.base_url + endpoint
        response = await self.client.post(url, headers=self.headers, json=json_payload)

        if response.status_code == 200:
            return response.json()
        else:
            msg = f"Error ({response.status_code}): {response.text}"
            raise ConnectionError(msg)

    async def close(self) -> None:
        """
        Close the underlying asynchronous HTTP client.
        """
        await self.client.aclose()
