import asyncio

from src.consensus.config import ConsensusConfig
from src.router.async_client import AsyncOpenRouterClient


async def send_initial_round(
    client: AsyncOpenRouterClient, consensus_config: ConsensusConfig
) -> dict:
    """
    Asynchronously sends the initial prompt to each model and collects their responses.

    :param client: An instance of AsyncOpenRouterClient.
    :param consensus_config: An instance of ConsensusConfig.
    :return: A dictionary mapping model IDs to their response texts.
    """

    async def get_initial_response(model: str) -> tuple[str, str]:
        payload = {
            "model": model,
            "messages": consensus_config.initial_prompt,
            "max_tokens": consensus_config.max_tokens,
            "temperature": consensus_config.temperature,
        }
        response = await client.send_chat_completion(payload)
        text = response.get("choices", [])[0].get("message", {}).get("content", "")
        print(f"{model} has provided a response to the initial prompt.")
        return model, text

    tasks = [get_initial_response(model) for model in consensus_config.models]
    results = await asyncio.gather(*tasks)
    return {model: text for model, text in results}


async def send_improvement_round(
    client, consensus_config: ConsensusConfig, responses: dict
) -> dict:
    """
    Asynchronously sends the improved prompt (with aggregated responses) to each model.

    :param client: An instance of an asynchronous OpenRouter client.
    :param consensus_config: An instance of ConsensusConfig.
    :param responses: Dict mapping model IDs to their previous responses.
    :return: Dict mapping model IDs to their new responses.
    """
    from src.consensus.aggregator import concatenate_aggregator

    aggregated_response = concatenate_aggregator(responses)

    async def get_improved_response(model: str) -> tuple[str, str]:
        conversation = build_improvement_conversation(
            consensus_config, responses[model], aggregated_response
        )
        payload = {
            "model": model,
            "messages": conversation,
            "max_tokens": consensus_config.max_tokens,
            "temperature": consensus_config.temperature,
        }
        response = await client.send_chat_completion(payload)
        text = response.get("choices", [])[0].get("message", {}).get("content", "")
        print(f"{model} has provided a new response.")
        return model, text

    tasks = [get_improved_response(model) for model in consensus_config.models]
    results = await asyncio.gather(*tasks)
    return {model: text for model, text in results}
