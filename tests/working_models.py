import asyncio

import structlog

from flare_ai_consensus.router import (
    AsyncOpenRouterProvider,
    ChatRequest,
    CompletionRequest,
)
from flare_ai_consensus.settings import ModelConfig, settings
from flare_ai_consensus.utils import load_json, save_json

logger = structlog.get_logger(__name__)


async def _test_model_completion(
    provider: AsyncOpenRouterProvider,
    model: ModelConfig,
    test_prompt: str,
    api_endpoint: str,
    delay: float = 1.0,
) -> tuple[ModelConfig, bool]:
    """
    Asynchronously sends a test request for a model using the specified API endpoint.

    :param provider: An instance of AsyncOpenRouterProvider.
    :param model: A ModelConfig instance with model configuration
    :param test_prompt: The prompt to test.
    :param api_endpoint: Either "completion" or "chat_completion".
    :return: A tuple (model, works) where works is True if the API call succeeded.
    """
    model_id = model.model_id
    if not model_id:
        return (model, False)

    # Introduce a delay
    await asyncio.sleep(delay)

    # Handle completion endpoint
    if api_endpoint.lower() == "completion":
        completion_payload: CompletionRequest = {
            "model": model_id,
            "prompt": test_prompt,
            "max_tokens": model.max_tokens,
            "temperature": model.temperature,
        }
        response = await provider.send_completion(completion_payload)

    # Handle chat completion endpoint
    elif api_endpoint.lower() == "chat_completion":
        chat_payload: ChatRequest = {
            "model": model_id,
            "messages": [{"role": "user", "content": test_prompt}],
            "max_tokens": model.max_tokens,
            "temperature": model.temperature,
        }
        response = await provider.send_chat_completion(chat_payload)

    else:
        msg = f"Unsupported api_endpoint: {api_endpoint}"
        raise ValueError(msg)

    if "error" not in response:
        logger.info("model works", model_id=model_id, api_endpoint=api_endpoint)
        return (model, True)

    error_info = response.get("error", {})
    logger.exception(
        "testing model",
        model_id=model_id,
        api_endpoint=api_endpoint,
        error=error_info.get("message", "Unknown error"),
    )

    return (model, False)


async def filter_working_models(
    provider: AsyncOpenRouterProvider,
    free_models: list,
    test_prompt: str,
    api_endpoint: str,
) -> list:
    """
    Asynchronously tests each model in free_models with the given test
    prompt and API endpoint returning only those models that respond
    without an error.
    :param provider: An instance of AsyncOpenRouterProvider.
    :param free_models: A list of model dictionaries.
    :param test_prompt: The prompt to test.
    :param api_endpoint: Either "completion" or "chat_completion".
    :return: A list of models (dicts) that work with the specified API.
    """
    tasks = [
        _test_model_completion(provider, model, test_prompt, api_endpoint, delay=i * 3)
        for i, model in enumerate(free_models)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    working_models = []
    for result in results:
        if isinstance(result, Exception):
            continue
        model, works = result  # pyright: ignore [reportGeneralTypeIssues]
        if works:
            working_models.append(model)

    return working_models


async def main() -> None:
    # Load the free models from free_models.json.
    free_models_file = settings.data_path / "free_models.json"
    free_models = load_json(free_models_file).get("data", [])
    test_prompt = "Who is Ash Ketchum?"

    # Initialize the asynchronous OpenRouter provider.
    provider = AsyncOpenRouterProvider(
        api_key=settings.open_router_api_key, base_url=settings.open_router_base_url
    )

    # Filter free models that work with the completions endpoints.
    for endpoint in ["completion", "chat_completion"]:
        working_models = await filter_working_models(
            provider, free_models, test_prompt, endpoint
        )
        completion_output_file = (
            settings.data_path / f"free_working_{endpoint}_models.json"
        )
        save_json({"data": working_models}, completion_output_file)
        logger.info(
            "working models saved",
            endpoint=endpoint,
            completion_output_file=completion_output_file,
        )

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
