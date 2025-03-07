import asyncio

import structlog

from flare_ai_consensus.consensus.aggregator import async_centralized_llm_aggregator
from flare_ai_consensus.router import AsyncOpenRouterProvider, ChatRequest
from flare_ai_consensus.settings import ConsensusConfig, Message, ModelConfig
from flare_ai_consensus.utils import parse_chat_response

logger = structlog.get_logger(__name__)


async def run_consensus(
    provider: AsyncOpenRouterProvider,
    consensus_config: ConsensusConfig,
    initial_conversation: list[Message],
) -> str:
    """
    Asynchronously runs the consensus learning loop.

    :param provider: An instance of an AsyncOpenRouterProvider.
    :param consensus_config: An instance of ConsensusConfig.
    :param initial_conversation: the input user prompt with system instructions.

    Returns: aggregated response (str)
    All responses are stored in response_data and can be returned for future use.
    """
    response_data = {}
    response_data["initial_conversation"] = initial_conversation

    # Step 1: Initial round.
    responses = await send_round(
        provider, consensus_config, response_data["initial_conversation"]
    )
    aggregated_response = await async_centralized_llm_aggregator(
        provider, consensus_config.aggregator_config, responses
    )
    logger.info(
        "initial response aggregation complete", aggregated_response=aggregated_response
    )

    response_data["iteration_0"] = responses
    response_data["aggregate_0"] = aggregated_response

    # Step 2: Improvement rounds.
    for i in range(consensus_config.iterations):
        responses = await send_round(
            provider, consensus_config, initial_conversation, aggregated_response
        )
        aggregated_response = await async_centralized_llm_aggregator(
            provider, consensus_config.aggregator_config, responses
        )
        logger.info(
            "responses aggregated",
            iteration=i + 1,
            aggregated_response=aggregated_response,
        )

        response_data[f"iteration_{i + 1}"] = responses
        response_data[f"aggregate_{i + 1}"] = aggregated_response

    return aggregated_response


def _build_improvement_conversation(
    consensus_config: ConsensusConfig,
    initial_conversation: list[Message],
    aggregated_response: str,
) -> list[Message]:
    """Build an updated conversation using the consensus configuration.

    :param consensus_config: An instance of ConsensusConfig.
    :param initial_conversation: the input user prompt with system instructions.
    :param aggregated_response: The aggregated consensus response.
    :return: A list of messages for the updated conversation.
    """
    conversation = initial_conversation.copy()

    # Add aggregated response
    conversation.append(
        {
            "role": consensus_config.aggregated_prompt_type,
            "content": f"Consensus: {aggregated_response}",
        }
    )

    # Add new prompt as "user" message
    conversation.append(
        {"role": "user", "content": consensus_config.improvement_prompt}
    )
    return conversation


async def _get_response_for_model(
    provider: AsyncOpenRouterProvider,
    consensus_config: ConsensusConfig,
    model: ModelConfig,
    initial_conversation: list[Message],
    aggregated_response: str | None,
) -> tuple[str | None, str]:
    """
    Asynchronously sends a chat completion request for a given model.

    :param provider: An instance of an asynchronous OpenRouter provider.
    :param consensus_config: An instance of ConsensusConfig.
    :param model: A ModelConfig instance.
    :param initial_conversation: the input user prompt with system instructions.
    :param aggregated_response: The aggregated consensus response
        from the previous round (or None).
    :return: A tuple of (model_id, response text).
    """
    if not aggregated_response:
        # Use initial prompt for the first round.
        conversation = initial_conversation
        logger.info("sending initial prompt", model_id=model.model_id)
    else:
        # Build the improvement conversation.
        conversation = _build_improvement_conversation(
            consensus_config, initial_conversation, aggregated_response
        )
        logger.info("sending improvement prompt", model_id=model.model_id)

    payload: ChatRequest = {
        "model": model.model_id,
        "messages": conversation,
        "max_tokens": model.max_tokens,
        "temperature": model.temperature,
    }
    response = await provider.send_chat_completion(payload)
    text = parse_chat_response(response)
    logger.info("new response", model_id=model.model_id, response=text)
    return model.model_id, text


async def send_round(
    provider: AsyncOpenRouterProvider,
    consensus_config: ConsensusConfig,
    initial_conversation: list[Message],
    aggregated_response: str | None = None,
) -> dict:
    """
    Asynchronously sends a round of chat completion requests for all models.

    :param provider: An instance of an asynchronous OpenRouter provider.
    :param consensus_config: An instance of ConsensusConfig.
    :param initial_conversation: the input user prompt with system instructions.
    :param aggregated_response: The aggregated consensus response from the
        previous round (or None).
    :return: A dictionary mapping model IDs to their response texts.
    """
    tasks = [
        _get_response_for_model(
            provider, consensus_config, model, initial_conversation, aggregated_response
        )
        for model in consensus_config.models
    ]
    results = await asyncio.gather(*tasks)
    return dict(results)
