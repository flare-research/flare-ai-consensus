from src.router.client import OpenRouterClient


def send_prompt_completion(client: OpenRouterClient, payload: dict) -> dict:
    """
    Send the prompt to the completions endpoint for a specific model.

    """
    return client.send_completion(payload)