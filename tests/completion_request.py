from src.config import config
from src.router import requests
from src.router.client import OpenRouterClient
from src.utils.saving import save_json


if __name__ == "__main__":
    # Initialize the OpenRouter client.
    client = OpenRouterClient(
        api_key=config.open_router_api_key,
        base_url=config.open_router_base_url,
    )

    model_id = "qwen/qwen-vl-plus:free"
    prompt = "Who is the second best Pokemon trainer in the original 'Pokemon the Series'?"

    # Initialize payload
    payload = {
        "model": model_id,
        "prompt": prompt,
        "max_tokens": 1500,
        "temperature": 0.7
    }

    # Get response and save it
    try:
        print(f"Sending prompt to model {model_id} ...")
        response = requests.send_prompt_completion(client, payload)
        print(response.get("choices", [])[0].get("text", ""))

        output_file = config.data_path / "response.json"
        save_json(response, output_file)
    except Exception as e:
        print(f"Error for model {model_id}: {e}")

