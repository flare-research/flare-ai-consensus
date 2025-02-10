import asyncio
from src.config import config
from src.router.client import AsyncOpenRouterClient
from src.utils.loader import load_json
from src.utils.saver import save_json
from src.consensus.config import ModelConfig  # Not used here, but if needed later

async def _test_model_completion(
    client: AsyncOpenRouterClient,
    model: dict,
    test_prompt: str,
    api_endpoint: str,
    delay: float = 1.0,
) -> tuple[dict, bool]:
    """
    Asynchronously sends a test request for a model using the specified API endpoint.

    :param client: An instance of AsyncOpenRouterClient.
    :param model: A dict representing a model (expected to have keys "id", "max_tokens", "temperature").
    :param test_prompt: The prompt to test.
    :param api_endpoint: Either "completion" or "chat_completion".
    :return: A tuple (model, works) where works is True if the API call succeeded without an error.
    """
    model_id = model.get("id")
    if not model_id:
        return (model, False)

    # Build payload based on API endpoint.
    if api_endpoint.lower() == "completion":
        payload = {
            "model": model_id,
            "prompt": test_prompt,
            "max_tokens": model.get("max_tokens", 50),
            "temperature": model.get("temperature", 0.7),
        }
        send_func = client.send_completion
    elif api_endpoint.lower() == "chat_completion":
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": test_prompt}],
            "max_tokens": model.get("max_tokens", 50),
            "temperature": model.get("temperature", 0.7),
        }
        send_func = client.send_chat_completion
    else:
        raise ValueError(f"Unsupported api_endpoint: {api_endpoint}")

    # Introduce a delay
    await asyncio.sleep(delay)

    try:
        response = await send_func(payload)
        if "error" not in response:
            print(f"Model {model_id} works with {api_endpoint}!")
            return (model, True)
        else:
            error_info = response.get("error", {})
            print(f"Model {model_id} returned error in {api_endpoint}: {error_info.get('message', 'Unknown error')}")
            return (model, False)
    except Exception as e:
        print(f"Error testing model {model_id} with {api_endpoint}: {e}")
        return (model, False)


async def filter_working_models(
    client: AsyncOpenRouterClient,
    free_models: list,
    test_prompt: str,
    api_endpoint: str,
) -> list:
    """
    Asynchronously tests each model in free_models with the given test prompt and API endpoint,
    returning only those models that respond without an error.

    :param client: An instance of AsyncOpenRouterClient.
    :param free_models: A list of model dictionaries.
    :param test_prompt: The prompt to test.
    :param api_endpoint: Either "completion" or "chat_completion".
    :return: A list of models (dicts) that work with the specified API.
    """
    tasks = [
        _test_model_completion(client, model, test_prompt, api_endpoint, delay = i)
        for i, model in enumerate(free_models)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # Filter out any exceptions and only keep models where works is True.
    valid_models = [
        model for result in results
        if not isinstance(result, Exception) and result[1]
        for model in [result[0]]
    ]
    return valid_models


async def main() -> None:
    # Load the free models from free_models.json.
    free_models_file = config.data_path / "free_models.json"
    free_models = load_json(free_models_file).get("data", [])
    test_prompt = "Who is Ash Ketchum?"

    # Initialize the asynchronous OpenRouter client.
    client = AsyncOpenRouterClient(api_key=config.open_router_api_key, base_url=config.open_router_base_url)

    # Filter free models that work with the completions endpoint.
    working_completion_models = await filter_working_models(client, free_models, test_prompt, "completion")
    completion_output_file = config.data_path / "free_working_completion_models.json"
    save_json({"data": working_completion_models}, completion_output_file)
    print(f"\nWorking completion models saved to {completion_output_file}.\n")

    # Filter free models that work with the chat completions endpoint.
    working_chat_models = await filter_working_models(client, free_models, test_prompt, "chat_completion")
    chat_output_file = config.data_path / "free_working_chat_models.json"
    save_json({"data": working_chat_models}, chat_output_file)
    print(f"\nWorking chat models saved to {chat_output_file}.")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
