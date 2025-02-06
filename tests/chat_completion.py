import argparse

from src.config import config
from src.router.client import OpenRouterClient
from src.utils.saving import save_json
from src.router import requests  # This module should expose send_chat_completion


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send a chat prompt to the OpenRouter chat completions endpoint."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["default", "interactive"],
        default="default",
        help="Run in 'default' mode with predefined messages or 'interactive' mode for conversation.",
    )
    return parser.parse_args()


def default_mode(
    client: OpenRouterClient,
    initial_prompt: str,
    model_id: str,
    num_iterations: str,
    improvement_prompt: str,
) -> None:
    """Run the chat completion with a predefined set of messages."""
    # Set up the initial conversation with a user prompt.
    conversation = [{"role": "user", "content": initial_prompt}]

    for i in range(num_iterations):
        payload = {
            "model": model_id,
            "messages": conversation,
            "max_tokens": 1500,
            "temperature": 0.7,
        }
        try:
            print(f"\nIteration {i + 1}: Sending conversation to model {model_id} ...")
            response = requests.send_chat_completion(client, payload)
            # Extract the assistant's response.
            assistant_response = (
                response.get("choices", [])[0].get("message", {}).get("content", "")
            )
            print(f"Assistant Response (Iteration {i + 1}):")
            print(assistant_response)

            # Append the assistant's response to the conversation history.
            conversation.append({"role": "assistant", "content": assistant_response})

            # Ask for improved response
            if i < num_iterations - 1:
                conversation.append({"role": "user", "content": improvement_prompt})
        except Exception as e:
            print(f"Error for model {model_id} in iteration {i + 1}: {e}")
            break

    # Save the final conversation to a file.
    output_file = config.data_path / "chat_response.json"
    save_json({"conversation": conversation}, output_file)
    print(f"\nFinal conversation saved to {output_file}")


def interactive_mode(client: OpenRouterClient, model_id: str) -> None:
    """Run the chat in interactive mode."""
    conversation = []
    print("Interactive mode. Type 'exit' to quit.")

    while True:
        user_input = input("\nEnter your 'user' prompt: ")
        if user_input.strip().lower() == "exit":
            print("Exiting interactive mode.")
            break

        conversation.append({"role": "user", "content": user_input})

        payload = {
            "model": model_id,
            "messages": conversation,
            "max_tokens": 1500,
            "temperature": 0.7,
        }

        try:
            response = requests.send_chat_completion(client, payload)
            assistant_msg = (
                response.get("choices", [])[0].get("message", {}).get("content", "")
            )
            print("\nAssistant:")
            print(assistant_msg)
            conversation.append({"role": "assistant", "content": assistant_msg})
        except Exception as e:
            print(f"Error for model {model_id}: {e}")


def main() -> None:
    args = parse_arguments()

    # Initialize the OpenRouter client.
    client = OpenRouterClient(
        api_key=config.open_router_api_key,
        base_url=config.open_router_base_url,
    )

    model_id = "qwen/qwen-vl-plus:free"

    if args.mode == "default":
        initial_prompt = "Who is the second best Pokemon trainer in the original 'Pokemon the Series'?"
        improvement_prompt = (
            "Can you improve on your previous answers with more precise arguments?"
        )

        default_mode(
            client,
            initial_prompt,
            model_id,
            3,
            improvement_prompt,
        )
    elif args.mode == "interactive":
        interactive_mode(client, model_id)
    else:
        print("Invalid mode. Please choose 'default' or 'interactive'.")


if __name__ == "__main__":
    main()
