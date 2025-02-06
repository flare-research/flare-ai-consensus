def concatenate_aggregator(responses: dict) -> str:
    """
    Aggregate responses by concatenating each model's answer with a label.

    :param responses: A dictionary mapping model IDs to their response texts.
    :return: A single aggregated string.
    """
    return "\n\n".join([f"{model}: {text}" for model, text in responses.items()])
