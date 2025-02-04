import requests


class BaseClient:
    """A base class to handle HTTP requests and common logic for API interaction."""
    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.headers = {"accept": "application/json"}

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        """Make a GET request to the API and return JSON response."""
        params = params or {}
        # If an API key is needed, it can be injected here.
        if self.api_key:
            params["api_key"] = self.api_key

        url = self.base_url + endpoint
        response = self.session.get(url=url, params=params, headers=self.headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            msg = f"Error ({response.status_code}): {response.text}"
            raise ConnectionError(msg)

