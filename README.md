[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

# Consensus Learning with LLMs

This repository offers a Python implementation of a single-node multi-model Consensus Learning (CL) framework.
CL is a decentralized ensemble learning paradigm introduced in [2402.16157](https://arxiv.org/abs/2402.16157).
The current implementation is a centralized version of CL specialized for Large Language Models (LLMs), done through OpenAI's [OpenRouter](https://openrouter.ai/docs/quick-start).
This provides access to more than 300 models through a unique interface.

## Repository Setup

[uv](https://docs.astral.sh/uv/getting-started/installation/) is used for dependency management.
To install all dependencies, run:

```bash
uv sync --all-extras
```

To add new dependencies, use `uv add <dependency>`.
For formatting and linting use:

```bash
uv run ruff format
uv run ruff check
```

## OpenAI API Key

Generate an [OpenRouter API key](https://openrouter.ai/settings/keys) and add it to the `env` variables.
You can check your available credits running:

```bash
uv run python -m tests.credits
```

## OpenRouter Endpoints

You can obtain a list of all models, and a separate list of all free models supported by OpenRouter by running:

```bash
uv run python -m tests.models
```

This will generate two `json` files in a data folder within the root directory.
The two main endpoints for interacting with the models are:

* **Completion Endpoint**: this is used for generating text completions in a non-conversational, single-prompt format.
This functionality can be tested by running (the `--prompt` and `--model` arguments are optional and can be also set directly in `tests/completion.py`):

```bash
uv run python -m tests.completion --prompt "Who is Ash Ketchum?" --model "google/learnlm-1.5-pro-experimental:free"
```

* **Chat Completion Endpoint**: this is designed for conversational interactions, and thus maintains a conversation history.
All messages must include a role:
  * `system`: used for providing context to a prompt.
  * `user`: these are messages that include the queries for the model.
  * `assistant`: models will generate responses with this role assigned. In addition to this, any message with this role will be considered as responses provided by the model in a previous turn.
This endpoint can be tested by running:

```bash
uv run python -m tests.chat_completion --mode default
```

When running the `default` mode, a set of predefined prompts will be used. In the `interactive` mode you can manually enter new `user` prompts, with any previous model responses being kept as `assistant` responses.

