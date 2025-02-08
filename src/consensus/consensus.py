from src.consensus.config import (
    ConsensusConfig,
    ModelConfig,
)
from src.router.client import OpenRouterClient
from src.utils import parser


def send_prompt(
    client: OpenRouterClient,
    model: ModelConfig,
    conversation: list[dict],
) -> str:
    """
    Send chat completion request for a specific model.

    :param client: An instance of OpenRouterClient.
    :param consensus_config: An instance of ConsensusConfig.
    :param model: The model id.
    :param conversation: A list of instructions for the model.
    :return: A dict mapping model IDs to their response texts.
    """
    # Format the request
    payload = {
        "model": model.model_id,
        "messages": conversation,
        "max_tokens": model.max_tokens,
        "temperature": model.temperature,
    }

    # Get response
    response = client.send_chat_completion(payload)
    print(f"{model.model_id} has provided a new response.")

    return parser.parse_chat_response(response)


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


def send_round(
    client: OpenRouterClient,
    consensus_config: ConsensusConfig,
    aggregated_response: str = None,
) -> dict:
    """
    Sends a round of chat completion requests for all models.
    If `aggregated_response` is not provided, the initial prompt is used.

    :param client: An instance of OpenRouterClient.
    :param consensus_config: An instance of ConsensusConfig.
    :param aggregated_response: The aggregated consensus from the previous round (or None).
    :return: A dictionary mapping model IDs to their response texts.
    """
    responses = {}
    for model in consensus_config.models:
        if aggregated_response is None:
            # For the initial round, use the initial conversation.
            conversation = consensus_config.initial_prompt
            print(f"Sending initial prompt to {model.model_id}.")
        else:
            # For improvement rounds, build an updated conversation.
            conversation = build_improvement_conversation(consensus_config, aggregated_response)
            print(f"Sending improvement prompt to {model.model_id}.")
        responses[model.model_id] = send_prompt(client, model, conversation)
    return responses
