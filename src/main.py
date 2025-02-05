from src.config import config
from src.router.client import OpenRouterClient


def main():
    # Set OpenRouter base url
    openrouter_base_url = "https://api.openrouter.example.com"

    # Initialize OpenRouter client
    client = OpenRouterClient(
        base_url=openrouter_base_url, api_key=config.open_router_api_key
    )

    # Send a query to the OpenRouter (which routes to multiple models)
    prompt = "Explain the benefits of consensus learning in AI."

    # If your OpenRouter API allows additional parameters, pass them here
    response_data = client.send_query(prompt)

    # Let's assume response_data contains multiple model outputs in a key "responses"
    # responses = response_data.get("responses", [])

    # Use the aggregator to consolidate these responses into a consensus answer
    # aggregator = ConsensusAggregator(entropy_threshold=0.5)
    # consensus_response = aggregator.aggregate(responses)

    # print("Consensus Response:")
    print(response_data)


if __name__ == "__main__":
    main()
