async def send_completion(client, payload: dict) -> dict:
    """
    Asynchronously send the prompt to the completions endpoint for a specific model.

    :param client: An instance of AsyncOpenRouterClient.
    :param payload: The JSON payload to send.
    :return: The JSON response as a dictionary.
    """
    return await client.send_completion(payload)


async def send_chat_completion(client, payload: dict) -> dict:
    """
    Asynchronously send the prompt to the chat completions endpoint for a specific model.

    :param client: An instance of AsyncOpenRouterClient.
    :param payload: The JSON payload to send.
    :return: The JSON response as a dictionary.
    """
    return await client.send_chat_completion(payload)
