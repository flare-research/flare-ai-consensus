from src.consensus.config import ConsensusConfig
from src.router.client import OpenRouterClient


def concatenate_aggregator(responses: dict) -> str:
    """
    Aggregate responses by concatenating each model's answer with a label.

    :param responses: A dictionary mapping model IDs to their response texts.
    :return: A single aggregated string.
    """
    return "\n\n".join([f"{model}: {text}" for model, text in responses.items()])


def centralized_llm_aggregator(
    client: OpenRouterClient,
    consensus_config: ConsensusConfig,
    aggregated_responses: str,
) -> str:
    """Use a centralized LLM  to combine responses.

    :param client: An OpenRouterClient instance.
    :param consensus_config: An instance of ConsensusConfig.
    :param aggregated_responses: A string containing aggregated responses from individual models.
    :return: The aggregator's combined response.
    """
    # Build the message list.
    messages = []
    messages.extend(consensus_config.aggregator.context)

    # Add a system message with the aggregated responses.
    messages.append(
        {"role": "system", "content": f"Aggregated responses:\n{aggregated_responses}"}
    )

    # Add the aggregator prompt
    messages.extend(consensus_config.aggregator.prompt)

    payload = {
        "model": consensus_config.aggregator.model,
        "messages": messages,
        "max_tokens": consensus_config.max_tokens,
        "temperature": consensus_config.temperature,
    }

    # Get aggregated response from the centralized LLM
    response = client.send_chat_completion(payload)
    aggregated_text = (
        response.get("choices", [])[0].get("message", {}).get("content", "")
    )
    return aggregated_text
