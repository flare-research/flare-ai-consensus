import asyncio

from src.config import config
from src.consensus import aggregator, consensus
from src.consensus.config import ConsensusConfig
from src.router.client import AsyncOpenRouterClient
from src.utils import (
    saver,
    loader,
)


async def run_consensus(
    client: AsyncOpenRouterClient,
    consensus_config: ConsensusConfig,
) -> None:
    """
    Asynchronously runs the consensus learning loop.

    :param client: An instance of a synchronous OpenRouterClient (used for aggregation).
    :param async_client: An instance of an asynchronous OpenRouterClient.
    :param consensus_config: An instance of ConsensusConfig.
    """
    # Step 1: Initial round.
    responses = await consensus.send_round(client, consensus_config)
    aggregated_response = await aggregator.async_centralized_llm_aggregator(
        client, consensus_config.aggregator_config, responses
    )
    print("\nInitial responses have been aggregated.")

    # Step 2: Improvement rounds.
    for i in range(consensus_config.iterations):
        responses = await consensus.send_round(
            client, consensus_config, aggregated_response
        )
        aggregated_response = await aggregator.async_centralized_llm_aggregator(
            client, consensus_config.aggregator_config, responses
        )
        print(f"\nThe responses have been aggregated after iteration {i + 1}:")

    # Step 3: Save final consensus.
    output_file = config.data_path / "final_consensus.json"
    saver.save_json(
        {"aggregated_response": aggregated_response, "responses": responses},
        output_file,
    )
    print(f"\nFinal consensus saved to {output_file}")

    # Close the async client to release resources.
    await client.close()


def main() -> None:
    # Load the consensus configuration from input.json
    config_json = loader.load_json(config.input_path / "input.json")
    consensus_config = ConsensusConfig.load_parameters(config_json)

    # Initialize the OpenRouter client.
    client = AsyncOpenRouterClient(
        api_key=config.open_router_api_key, base_url=config.open_router_base_url
    )

    # Run the consensus learning process with synchronous requests.
    asyncio.run(run_consensus(client, consensus_config))


if __name__ == "__main__":
    main()
