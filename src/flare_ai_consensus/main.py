import asyncio

import structlog

from flare_ai_consensus.config import config
from flare_ai_consensus.consensus import aggregator, consensus
from flare_ai_consensus.consensus.config import ConsensusConfig
from flare_ai_consensus.router.client import AsyncOpenRouterClient
from flare_ai_consensus.utils import (
    loader,
    saver,
)

logger = structlog.get_logger(__name__)


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
    response_data = {}
    response_data["initial_conversation"] = consensus_config.initial_prompt

    # Step 1: Initial round.
    responses = await consensus.send_round(client, consensus_config)
    aggregated_response = await aggregator.async_centralized_llm_aggregator(
        client, consensus_config.aggregator_config, responses
    )
    logger.info(
        "initial response aggregation complete", aggregated_response=aggregated_response
    )

    response_data["iteration_0"] = responses
    response_data["aggregate_0"] = aggregated_response

    # Step 2: Improvement rounds.
    for i in range(consensus_config.iterations):
        responses = await consensus.send_round(
            client, consensus_config, aggregated_response
        )
        aggregated_response = await aggregator.async_centralized_llm_aggregator(
            client, consensus_config.aggregator_config, responses
        )
        logger.info(
            "responses aggregated",
            iteration=i + 1,
            aggregated_response=aggregated_response,
        )

        response_data[f"iteration_{i + 1}"] = responses
        response_data[f"aggregate_{i + 1}"] = aggregated_response

    # Step 3: Save final consensus.
    output_file = config.data_path / "final_consensus.json"
    saver.save_json(
        response_data,
        output_file,
    )
    logger.info("saved consensus", output_file=output_file)

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
