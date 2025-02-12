import asyncio

from flare_ai_consensus.consensus.config import ConsensusConfig, ModelConfig
from flare_ai_consensus.router.client import AsyncOpenRouterClient
from flare_ai_consensus.utils.parser import parse_chat_response


def build_improvement_conversation(
    consensus_config: ConsensusConfig, aggregated_response: str
) -> list:
    """Build an updated conversation using the consensus configuration.

    :param consensus_config: An instance of ConsensusConfig.
    :param aggregated_response: The aggregated consensus response.
    :return: A list of messages for the updated conversation.
    """
    conversation = consensus_config.initial_prompt.copy()

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
    :param aggregated_response: The aggregated consensus response
        from the previous round (or None).
    :param model: A ModelConfig instance.
    :return: A tuple of (model_id, response text).
    """
    if aggregated_response is None:
        # Use initial prompt for the first round.
        conversation = consensus_config.initial_prompt
        print(f"Sending initial prompt to {model.model_id}.")
    else:
        # Build the improvement conversation.
        conversation = build_improvement_conversation(
            consensus_config, aggregated_response
        )
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
    aggregated_response: str | None = None,
) -> dict:
    """
    Asynchronously sends a round of chat completion requests for all models.

    :param client: An instance of an asynchronous OpenRouter client.
    :param consensus_config: An instance of ConsensusConfig.
    :param aggregated_response: The aggregated consensus response from the
        previous round (or None).
    :return: A dictionary mapping model IDs to their response texts.
    """
    tasks = [
        get_response_for_model(client, consensus_config, model, aggregated_response)
        for model in consensus_config.models
    ]
    results = await asyncio.gather(*tasks)
    return dict(results)
