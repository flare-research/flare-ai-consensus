import json
from pathlib import Path

from src.config import config
from src.router import requests
from src.router.client import OpenRouterClient
from src.utils import loader
from src.utils.saving import save_json

def get_selected_models(models_file: Path) -> list:
    """Read the selected model IDs from a JSON file."""
    data = loader.load_json(models_file)

    # Expecting the structure {"data": [list of model IDs]}
    return data.get("data", [])

def get_prompt(prompt_file: Path) -> str:
    """Read the prompt text from a file."""
    return loader.load_txt(prompt_file)


def aggregate_responses(responses: list) -> str:
    """Simple aggregation by concatenating all responses."""
    return "\n\n".join(responses)


def main():
    models_file = config.input_path / "selected_models.json"
    prompt_file = config.input_path / "prompt.txt"

    # Read selected models and prompt
    selected_models = get_selected_models(models_file)
    prompt = get_prompt(prompt_file)

    # Initialize the OpenRouter client with your configuration.
    client = OpenRouterClient(
        api_key=config.open_router_api_key,
        base_url=config.open_router_base_url,
    )

    # Send the prompt to every model in our selected list.
    for model_id in selected_models[:1]:
        print(f"Sending prompt to model {model_id} ...")
        try:
            payload = {
                "model": model_id,
                "prompt": prompt,
                "max_tokens": 1500,
                "temperature": 0.7
            }
            model_response = requests.send_prompt_completion(client, payload)
            print(model_response)
        except Exception as e:
            print(f"Error for model {model_id}: {e}")

    # # Aggregate responses simply by concatenation
    # aggregated_response = aggregate_responses(responses)

    # Prepare the output JSON
    output_json = {"aggregated_response": model_response}

    # Save the aggregated response to response.json in config.data_path
    output_file = config.data_path / "response.json"
    save_json(output_json, output_file)

if __name__ == "__main__":
    main()
