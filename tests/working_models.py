import asyncio

import structlog

from flare_ai_consensus.config import config
from flare_ai_consensus.router.client import AsyncOpenRouterClient
from flare_ai_consensus.utils.loader import load_json
from flare_ai_consensus.utils.saver import save_json

logger = structlog.get_logger(__name__)


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
    :param model: A dict representing a model (expected to have keys
        "id", "max_tokens", "temperature").
    :param test_prompt: The prompt to test.
    :param api_endpoint: Either "completion" or "chat_completion".
    :return: A tuple (model, works) where works is True if the API call
        succeeded without an error.
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
        msg = f"Unsupported api_endpoint: {api_endpoint}"
        raise ValueError(msg)

    # Introduce a delay
    await asyncio.sleep(delay)

    try:
        response = await send_func(payload)
        if "error" not in response:
            logger.info("model works", model_id=model_id, api_endpoint=api_endpoint)
            return (model, True)
        error_info = response.get("error", {})
        logger.error(
            "testing model",
            model_id=model_id,
            api_endpoint=api_endpoint,
            error=error_info.get("message", "Unknown error"),
        )
    except Exception:
        logger.exception("testing model", model_id=model_id, api_endpoint=api_endpoint)
        return (model, False)
    else:
        return (model, False)


async def filter_working_models(
    client: AsyncOpenRouterClient,
    free_models: list,
    test_prompt: str,
    api_endpoint: str,
) -> list:
    """
    Asynchronously tests each model in free_models with the given test
    prompt and API endpoint returning only those models that respond
    without an error.

    :param client: An instance of AsyncOpenRouterClient.
    :param free_models: A list of model dictionaries.
    :param test_prompt: The prompt to test.
    :param api_endpoint: Either "completion" or "chat_completion".
    :return: A list of models (dicts) that work with the specified API.
    """
    tasks = [
        _test_model_completion(client, model, test_prompt, api_endpoint, delay=i * 3)
        for i, model in enumerate(free_models)
    ]
    results = await asyncio.gather(*tasks)

    valid_models = []
    for result in results:
        if isinstance(result, Exception):
            continue
        model, works = result
        if works:
            valid_models.append(model)
    return valid_models


async def main() -> None:
    # Load the free models from free_models.json.
    free_models_file = config.data_path / "free_models.json"
    free_models = load_json(free_models_file).get("data", [])
    test_prompt = "Who is Ash Ketchum?"

    # Initialize the asynchronous OpenRouter client.
    client = AsyncOpenRouterClient(
        api_key=config.open_router_api_key, base_url=config.open_router_base_url
    )

    # Filter free models that work with the completions endpoints.
    for endpoint in ["completion", "chat_completion"]:
        working_models = await filter_working_models(
            client, free_models, test_prompt, endpoint
        )
        completion_output_file = (
            config.data_path / f"free_working_{endpoint}_models.json"
        )
        save_json({"data": working_models}, completion_output_file)
        logger.info(
            "working models saved",
            endpoint=endpoint,
            completion_output_file=completion_output_file,
        )

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
