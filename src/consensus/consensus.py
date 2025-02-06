from src.consensus.config import ConsensusConfig


def send_initial_round(client, consensus_config: ConsensusConfig) -> dict:
    """Send the initial prompt to each model.

    :param client: An instance of OpenRouterClient.
    :param consensus_config: An instance of ConsensusConfig.
    :return: A dict mapping model IDs to their response texts.
    """
    responses = {}
    for model in consensus_config.models:
        payload = {
            "model": model,
            "messages": consensus_config.initial_prompt,
            "max_tokens": consensus_config.max_tokens,
            "temperature": consensus_config.temperature,
        }
        response = client.send_chat_completion(payload)
        text = response.get("choices", [])[0].get("message", {}).get("content", "")
        responses[model] = text
        print(f"{model} has provided a response to the initial prompt.")
    return responses


def build_improvement_conversation(
    consensus_config: ConsensusConfig, previous_response: str, aggregated_response: str
) -> list:
    """Build an updated conversation using the consensus configuration.

    :param consensus_config: An instance of ConsensusConfig.
    :param previous_response: The model's previous answer.
    :param aggregated_response: The aggregated consensus response.
    :return: A list of messages for the updated conversation.
    """
    conversation = consensus_config.initial_prompt.copy()

    # Add previous response as "assistant" message
    conversation.append({"role": "assistant", "content": previous_response})

    # Add aggregated response
    conversation.append(
        {
            "role": consensus_config.new_prompt_type,
            "content": f"Consensus: {aggregated_response}",
        }
    )

    # Add new prompt as "user" message
    conversation.append(
        {"role": "user", "content": consensus_config.improvement_prompt}
    )
    return conversation


def send_improvement_round(
    client, consensus_config: ConsensusConfig, responses: dict
) -> dict:
    """For each model, build an updated conversation and send it.

    :param client: An instance of OpenRouterClient.
    :param consensus_config: An instance of ConsensusConfig.
    :param responses: Dict mapping model IDs to their previous responses.
    :return: Dict mapping model IDs to their new responses.
    """
    new_responses = {}
    from src.consensus.aggregator import concatenate_aggregator

    aggregated_response = concatenate_aggregator(responses)
    for model in consensus_config.models:
        conversation = build_improvement_conversation(
            consensus_config, responses[model], aggregated_response
        )
        payload = {
            "model": model,
            "messages": conversation,
            "max_tokens": consensus_config.max_tokens,
            "temperature": consensus_config.temperature,
        }
        response = client.send_chat_completion(payload)
        text = response.get("choices", [])[0].get("message", {}).get("content", "")
        new_responses[model] = text
        print(f"{model} has provided a new response.")
    return new_responses
