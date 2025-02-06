from src.config import config
from src.consensus import (
    aggregator,
    consensus,
)
from src.consensus.config import ConsensusConfig
from src.router.client import OpenRouterClient
from src.utils import (
    saving,
    loader,
)


def run_consensus(client: OpenRouterClient, consensus_config: ConsensusConfig) -> None:
    """Run the consensus learning loop using the provided client and consensus configuration.

    :param client: An instance of OpenRouterClient.
    :param consensus_config: An instance of ConsensusConfig.
    """
    # Step 1. Get initial responses and aggregate them
    responses = consensus.send_initial_round(client, consensus_config)
    aggregated_response = aggregator.concatenate_aggregator(responses)
    print("Initial Aggregated Response:")
    print(aggregated_response)

    # Step 2. Iterative improvement rounds.
    for i in range(consensus_config.iterations):
        responses = consensus.send_improvement_round(
            client, consensus_config, responses
        )
        aggregated_response = aggregator.concatenate_aggregator(responses)
        print(f"\nAggregated Response after iteration {i + 1}:")
        print(aggregated_response)

    # Save the final consensus.
    output_file = config.data_path / "final_consensus.json"
    saving.save_json(
        {"aggregated_response": aggregated_response, "responses": responses},
        output_file,
    )
    print(f"\nFinal consensus saved to {output_file}")


def main() -> None:
    # Load the consensus configuration from input.json
    config_json = loader.load_json(config.input_path / "input.json")
    consensus_config = ConsensusConfig.load_parameters(config_json)

    # Initialize the OpenRouter client.
    client = OpenRouterClient(
        api_key=config.open_router_api_key, base_url=config.open_router_base_url
    )

    # Run the consensus learning process.
    run_consensus(client, consensus_config)


if __name__ == "__main__":
    main()
