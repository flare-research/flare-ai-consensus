from src.config import config
from src.router.client import OpenRouterClient
from src.utils.loader import load_json
from src.utils.saving import save_json


def filter_working_models(
    client: OpenRouterClient, free_models: list, test_prompt: str
) -> list:
    """
    Send test completion requests and keep working models.

    :param client: An initialized OpenRouterClient.
    :param free_models: A list of free model dictionaries.
    :param test_prompt: A sample prompt used for the models.
    :return: A list of free models that work with the completion API.
    """
    valid_models = []

    for model in free_models:
        model_id = model.get("id")
        if not model_id:
            continue

        payload = {
            "model": model_id,
            "prompt": test_prompt,
            "max_tokens": 50,
            "temperature": 0.7,
        }

        try:
            response = client.send_completion(payload)
            # Check if an error is present in the response.
            if "error" not in response:
                print(f"Model {model_id} works with completion!")
                valid_models.append(model)
            else:
                error_info = response.get("error", {})
                print(
                    f"Model {model_id} returned error in completion: {error_info.get('message', 'Unknown error')}"
                )
        except Exception as e:
            print(f"Error testing model {model_id} with completion: {e}")

    return valid_models


def filter_working_chat_models(
    client: OpenRouterClient, free_models: list, test_prompt: str
) -> list:
    """
    Send test chat completion requests and keep working models.

    :param client: An initialized OpenRouterClient.
    :param free_models: A list of free model dictionaries.
    :param test_prompt: A sample prompt used for the models.
    :return: A list of free models that work with the chat completions API.
    """
    valid_models = []

    for model in free_models:
        model_id = model.get("id")
        if not model_id:
            continue

        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": test_prompt}],
            "max_tokens": 50,
            "temperature": 0.7,
        }

        try:
            response = client.send_chat_completion(payload)
            # Check if an error is present in the response.
            if "error" not in response:
                print(f"Model {model_id} works with chat completion!")
                valid_models.append(model)
            else:
                error_info = response.get("error", {})
                print(
                    f"Model {model_id} returned error in chat: {error_info.get('message', 'Unknown error')}"
                )
        except Exception as e:
            print(f"Error testing model {model_id} with chat: {e}")

    return valid_models


def main() -> None:
    # Load the free models from free_models.json.
    free_models_file = config.data_path / "free_models.json"
    free_models = load_json(free_models_file).get("data", [])
    test_prompt = "Who is Ash Ketchum?"

    # Initialize the OpenRouter client.
    client = OpenRouterClient(
        api_key=config.open_router_api_key, base_url=config.open_router_base_url
    )

    # Filter free models that work with the completions endpoint.
    working_completion_models = filter_working_models(client, free_models, test_prompt)
    completion_output_file = config.data_path / "free_working_completion_models.json"
    save_json({"data": working_completion_models}, completion_output_file)
    print(f"\nWorking completion models saved to {completion_output_file}")

    # Filter free models that work with the chat completions endpoint.
    working_chat_models = filter_working_chat_models(client, free_models, test_prompt)
    chat_output_file = config.data_path / "free_working_chat_models.json"
    save_json({"data": working_chat_models}, chat_output_file)
    print(f"\nWorking chat models saved to {chat_output_file}")


if __name__ == "__main__":
    main()
