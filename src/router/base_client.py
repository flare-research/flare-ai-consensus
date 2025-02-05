import requests

class BaseClient:
    """A base class to handle HTTP requests and common logic for API interaction."""

    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        """
        :param base_url: The base URL for the API.
        :param api_key: Optional API key for authentication.
        """
        self.base_url = base_url.rstrip("/")  # Ensure no trailing slash
        self.api_key = api_key
        self.session = requests.Session()
        # Set up headers: include the Authorization header if an API key is provided.
        self.headers = {"accept": "application/json"}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        """
        Make a GET request to the API and return the JSON response.

        :param endpoint: The API endpoint (should begin with a slash, e.g., "/models").
        :param params: Optional query parameters.
        :return: JSON response as a dictionary.
        """
        params = params or {}

        url = self.base_url + endpoint
        response = self.session.get(
            url=url,
            params=params,
            headers=self.headers,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()
        else:
            msg = f"Error ({response.status_code}): {response.text}"
            raise ConnectionError(msg)
