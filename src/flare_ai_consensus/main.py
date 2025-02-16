import asyncio

import structlog

from flare_ai_consensus.consensus import (
    async_centralized_llm_aggregator,
    send_round,
)
from flare_ai_consensus.router import AsyncOpenRouterProvider
from flare_ai_consensus.settings import ConsensusConfig, settings
from flare_ai_consensus.utils import load_json, save_json

logger = structlog.get_logger(__name__)


async def run_consensus(
    provider: AsyncOpenRouterProvider,
    consensus_config: ConsensusConfig,
) -> None:
    """
    Asynchronously runs the consensus learning loop.

    :param provider: An instance of a OpenRouterProvider (used for aggregation).
    :param async_provider: An instance of an AsyncOpenRouterProvider.
    :param consensus_config: An instance of ConsensusConfig.
    """
    response_data = {}
    response_data["initial_conversation"] = consensus_config.initial_prompt

    # Step 1: Initial round.
    responses = await send_round(provider, consensus_config)
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
        responses = await send_round(provider, consensus_config, aggregated_response)
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

    # Step 3: Save final consensus.
    output_file = settings.data_path / "final_consensus.json"
    save_json(
        response_data,
        output_file,
    )
    logger.info("saved consensus", output_file=output_file)

    # Close the async provider to release resources.
    await provider.close()


def main() -> None:
    # Load the consensus configuration from input.json
    config_json = load_json(settings.input_path / "input.json")
    settings.load_consensus_config(config_json)

    # Initialize the OpenRouter provider.
    provider = AsyncOpenRouterProvider(
        api_key=settings.open_router_api_key, base_url=settings.open_router_base_url
    )

    # Run the consensus learning process with synchronous requests.
    if settings.consensus_config:
        asyncio.run(run_consensus(provider, settings.consensus_config))


if __name__ == "__main__":
    main()
