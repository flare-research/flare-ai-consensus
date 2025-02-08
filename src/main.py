import asyncio

from src.config import config
from src.consensus import (
    aggregator,
    async_consensus,
    consensus
)
from src.consensus.config import ConsensusConfig
from src.router.client import OpenRouterClient
from src.router.async_client import AsyncOpenRouterClient
from src.utils import (
    saver,
    loader,
)
from src.consensus.async_consensus import send_round


def run_sync_consensus(
    client: OpenRouterClient, consensus_config: ConsensusConfig
) -> None:
    """Consensus learning loop with synchronous requests."""
    # Step 1. Get initial responses.
    responses = consensus.send_round(client, consensus_config)

    # Step 2. Aggregate responses with chosen method.
    aggregated_response = aggregator.centralized_llm_aggregator(
        client, consensus_config.aggregator_config, responses
    )
    print("\nInitial responses have been aggregated.")

    # Step 3. Iterative improvement rounds.
    for i in range(consensus_config.iterations):
        # Step 3a. Get new responses.
        responses = consensus.send_round(
            client, consensus_config, aggregated_response
        )

        # Step 3b. Aggregate new responses
        aggregated_response = aggregator.centralized_llm_aggregator(
            client, consensus_config.aggregator_config, responses
        )
        print(f"\nThe responses have been aggregated after iteration {i + 1}.")

    # Step 4. Save the final consensus output.
    output_file = config.data_path / "final_consensus.json"
    saver.save_json(
        {"aggregated_response": aggregated_response, "responses": responses},
        output_file,
    )
    print(f"\n{aggregated_response}")


async def run_async_consensus(
    client: OpenRouterClient,
    async_client: AsyncOpenRouterClient,
    consensus_config: ConsensusConfig,
) -> None:
    """
    Asynchronously runs the consensus learning loop.

    :param client: An instance of a synchronous OpenRouterClient (used for aggregation).
    :param async_client: An instance of an asynchronous OpenRouterClient.
    :param consensus_config: An instance of ConsensusConfig.
    """
    # Step 1: Initial round.
    responses = await send_round(async_client, consensus_config)
    aggregated_response = aggregator.centralized_llm_aggregator(
        client, consensus_config.aggregator_config, responses
    )
    print("\nInitial responses have been aggregated:")

    # Step 2: Improvement rounds.
    for i in range(consensus_config.iterations):
        responses = await send_round(async_client, consensus_config, aggregated_response)
        aggregated_response = aggregator.centralized_llm_aggregator(
            client, consensus_config.aggregator_config, responses
        )
        print(f"\nThe responses have been aggregated after iteration {i + 1}:")

    # Step 3: Save final consensus.
    output_file = config.data_path / "final_consensus.json"
    saver.save_json({"aggregated_response": aggregated_response, "responses": responses}, output_file)
    print(f"\nFinal consensus saved to {output_file}")


def main() -> None:
    # Load the consensus configuration from input.json
    config_json = loader.load_json(config.input_path / "input.json")
    consensus_config = ConsensusConfig.load_parameters(config_json)

    # Initialize the OpenRouter client.
    client = OpenRouterClient(
        api_key=config.open_router_api_key, base_url=config.open_router_base_url
    )
    async_client = AsyncOpenRouterClient(
        api_key=config.open_router_api_key, base_url=config.open_router_base_url
    )

    # Run the consensus learning process with synchronous requests.
    asyncio.run(run_async_consensus(client, async_client, consensus_config))

if __name__ == "__main__":
    main()
