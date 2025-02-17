import argparse

import structlog

from flare_ai_consensus.router import CompletionRequest, OpenRouterProvider
from flare_ai_consensus.settings import settings
from flare_ai_consensus.utils import save_json

logger = structlog.get_logger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments and return the parsed namespace."""
    parser = argparse.ArgumentParser(
        description="Send a prompt to the OpenRouter completion endpoint."
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="Who is the second best Pokemon trainer in the original"
        "'Pokemon the Series'?",
        help="The prompt to send to the model. "
        "Enclose it in quotes if it contains spaces.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="google/gemini-2.0-flash-exp:free",
        help="The model ID to use (default: google/gemini-2.0-flash-exp:free).",
    )
    return parser.parse_args()


def send_prompt(provider: OpenRouterProvider, model_id: str, prompt: str) -> dict:
    """
    Send a prompt to the model using the completions endpoint.

    :param provider: An instance of OpenRouterProvder.
    :param model_id: The model ID to use.
    :param prompt: The text prompt to send.
    :return: The JSON response from the API.
    """
    payload: CompletionRequest = {
        "model": model_id,
        "prompt": prompt,
        "max_tokens": 1500,
        "temperature": 0.7,
    }
    return provider.send_completion(payload)


def start_chat(args: argparse.Namespace) -> None:
    """Start chat with the selected model."""
    model_id = args.model
    prompt = args.prompt

    # Initialize the OpenRouter provider
    provider = OpenRouterProvider(
        api_key=settings.open_router_api_key,
        base_url=settings.open_router_base_url,
    )

    try:
        logger.info("sending prompt", model_id=model_id, prompt=prompt)
        response = send_prompt(provider, model_id, prompt)

        # Save the full JSON response to a file.
        output_file = settings.data_path / "response.json"
        save_json(response, output_file)

        # Log the response
        response_text = response.get("choices", [])[0].get("text", "")
        logger.info("model response", response_text=response_text)

    except Exception as e:
        logger.exception("error", model_id=model_id, error=e)


def main() -> None:
    args = parse_arguments()
    start_chat(args)


if __name__ == "__main__":
    main()
