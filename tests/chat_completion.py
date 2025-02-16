import argparse

import structlog

from flare_ai_consensus.router import ChatRequest, OpenRouterProvider
from flare_ai_consensus.settings import settings
from flare_ai_consensus.utils import save_json

logger = structlog.get_logger(__name__)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send a chat prompt to the OpenRouter chat completions endpoint."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["default", "interactive"],
        default="default",
        help="Run in 'default' mode with predefined messages"
        "or 'interactive' mode for conversation.",
    )
    return parser.parse_args()


def default_mode(
    provider: OpenRouterProvider,
    initial_conversation: list[dict],
    model_id: str,
    num_iterations: int,
    improvement_prompt: str,
) -> None:
    """Run the chat completion with a predefined set of messages."""
    # Set up the initial conversation with a user prompt.
    conversation = []
    conversation.extend(initial_conversation)

    for i in range(num_iterations):
        payload: ChatRequest = {
            "model": model_id,
            "messages": conversation,
            "max_tokens": 1500,
            "temperature": 0.7,
        }
        try:
            logger.info("sending conversation", model_id=model_id, iteration=i + 1)
            response = provider.send_chat_completion(payload)
            # Extract the assistant's response.
            assistant_response = (
                response.get("choices", [])[0].get("message", {}).get("content", "")
            )
            logger.info(
                "assistant response",
                iteration=i + 1,
                assistant_response=assistant_response,
            )

            # Append the assistant's response to the conversation history.
            conversation.append({"role": "assistant", "content": assistant_response})

            # Ask for improved response
            if i < num_iterations - 1:
                conversation.append({"role": "user", "content": improvement_prompt})
        except Exception:
            logger.exception("error", model_id=model_id, iteration=i + 1)
            break

    # Save the final conversation to a file.
    output_file = settings.data_path / "chat_response.json"
    save_json({"conversation": conversation}, output_file)
    logger.info("final conversation saved", output_file=output_file)


def interactive_mode(provider: OpenRouterProvider, model_id: str) -> None:
    """Run the chat in interactive mode."""
    conversation = []
    print("Interactive mode. Type 'exit' to quit.")  # noqa: T201

    while True:
        user_input = input("\nEnter your 'user' prompt: ")
        if user_input.strip().lower() == "exit":
            print("Exiting interactive mode.")  # noqa: T201
            break

        conversation.append({"role": "user", "content": user_input})

        payload: ChatRequest = {
            "model": model_id,
            "messages": conversation,
            "max_tokens": 1500,
            "temperature": 0.7,
        }

        try:
            response = provider.send_chat_completion(payload)
            assistant_msg = (
                response.get("choices", [])[0].get("message", {}).get("content", "")
            )
            print("\nAssistant:")  # noqa: T201
            print(assistant_msg)  # noqa: T201
            conversation.append({"role": "assistant", "content": assistant_msg})
        except Exception as e:  # noqa: BLE001
            print(f"Error for model {model_id}: {e}")  # noqa: T201


def main() -> None:
    args = parse_arguments()

    # Initialize the OpenRouter provider
    provider = OpenRouterProvider(
        api_key=settings.open_router_api_key,
        base_url=settings.open_router_base_url,
    )

    model_id = "qwen/qwen-vl-plus:free"

    if args.mode == "default":
        initial_conversation = [
            {
                "role": "system",
                "content": "You are an expert on Pokemon. "
                "Provide concise and insightful answers.",
            },
            {
                "role": "user",
                "content": "Who is the second best Pokemon trainer"
                "in the original 'Pokemon the Series'?",
            },
        ]
        improvement_prompt = (
            "Can you improve on your previous answers with more precise arguments?"
        )

        default_mode(
            provider,
            initial_conversation,
            model_id,
            3,
            improvement_prompt,
        )
    elif args.mode == "interactive":
        interactive_mode(provider, model_id)
    else:
        logger.info("invalid mode: choose 'default' or 'interactive'")


if __name__ == "__main__":
    main()
