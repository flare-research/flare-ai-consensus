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
    """Run the consensus learning loop.

    :param client: An instance of OpenRouterClient.
    :param consensus_config: An instance of ConsensusConfig.
    """
    # Step 1. Get initial responses.
    responses = consensus.send_initial_round(client, consensus_config)

    # Step 2. Aggregate responses with chosen method.
    aggregated_response = aggregator.centralized_llm_aggregator(
        client, consensus_config.aggregator_config, responses
    )
    print("Initial responses have been aggregated.")

    # Step 3. Iterative improvement rounds.
    for i in range(consensus_config.iterations):
        # Step 3a. Get new responses.
        responses = consensus.send_improvement_round(
            client, consensus_config, aggregated_response
        )

        # Step 3b. Aggregate new responses
        aggregated_response = aggregator.centralized_llm_aggregator(
            client, consensus_config.aggregator_config, responses
        )
        print(f"\n The responses have been aggregated after iteration {i + 1}.")

    # Step 4. Save the final consensus output.
    output_file = config.data_path / "final_consensus.json"
    saving.save_json(
        {"aggregated_response": aggregated_response, "responses": responses},
        output_file,
    )
    print(f"\nFinal consensus saved to {output_file}.")


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
