import asyncio

from src.consensus.config import (
    ConsensusConfig,
    ModelConfig
)
from src.consensus.consensus import build_improvement_conversation
from src.router.async_client import AsyncOpenRouterClient
from src.utils.parser import parse_chat_response


async def get_response_for_model(
    client: AsyncOpenRouterClient,
    consensus_config: ConsensusConfig,
    model: ModelConfig,
    aggregated_response: str,
) -> tuple[str, str]:
    """
    Asynchronously sends a chat completion request for a given model.

    :param client: An instance of an asynchronous OpenRouter client.
    :param consensus_config: An instance of ConsensusConfig.
    :param aggregated_response: The aggregated consensus response from the previous round (or None).
    :param model: A ModelConfig instance.
    :return: A tuple of (model_id, response text).
    """
    if aggregated_response is None:
        # Use initial prompt for the first round.
        conversation = consensus_config.initial_prompt
        print(f"Sending initial prompt to {model.model_id}.")
    else:
        # Build the improvement conversation.
        conversation = build_improvement_conversation(consensus_config, aggregated_response)
        print(f"Sending improvement prompt to {model.model_id}.")

    payload = {
        "model": model.model_id,
        "messages": conversation,
        "max_tokens": model.max_tokens,
        "temperature": model.temperature,
    }
    response = await client.send_chat_completion(payload)
    text = parse_chat_response(response)
    print(f"{model.model_id} has provided a new response.")

    return model.model_id, text


async def send_round(
    client: AsyncOpenRouterClient,
    consensus_config: ConsensusConfig,
    aggregated_response: str = None,
) -> dict:
    """
    Asynchronously sends a round of chat completion requests for all models.

    :param client: An instance of an asynchronous OpenRouter client.
    :param consensus_config: An instance of ConsensusConfig.
    :param aggregated_response: The aggregated consensus response from the previous round (or None).
    :return: A dictionary mapping model IDs to their response texts.
    """
    tasks = [
        get_response_for_model(client, consensus_config, model, aggregated_response)
        for model in consensus_config.models
    ]
    results = await asyncio.gather(*tasks)
    return {model_id: text for model_id, text in results}
