[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Flare](https://img.shields.io/badge/flare-network-e62058.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNCIgaGVpZ2h0PSIzNCI+PHBhdGggZD0iTTkuNC0uMWEzMjAuMzUgMzIwLjM1IDAgMCAwIDIuOTkuMDJoMi4yOGExMTA2LjAxIDExMDYuMDEgMCAwIDEgOS4yMy4wNGMzLjM3IDAgNi43My4wMiAxMC4xLjA0di44N2wuMDEuNDljLS4wNSAyLTEuNDMgMy45LTIuOCA1LjI1YTkuNDMgOS40MyAwIDAgMS02IDIuMDdIMjAuOTJsLTIuMjItLjAxYTQxNjEuNTcgNDE2MS41NyAwIDAgMS04LjkyIDBMMCA4LjY0YTIzNy4zIDIzNy4zIDAgMCAxLS4wMS0xLjUxQy4wMyA1LjI2IDEuMTkgMy41NiAyLjQgMi4yIDQuNDcuMzcgNi43LS4xMiA5LjQxLS4wOXoiIGZpbGw9IiNFNTIwNTgiLz48cGF0aCBkPSJNNy42NSAxMi42NUg5LjJhNzU5LjQ4IDc1OS40OCAwIDAgMSA2LjM3LjAxaDMuMzdsNi42MS4wMWE4LjU0IDguNTQgMCAwIDEtMi40MSA2LjI0Yy0yLjY5IDIuNDktNS42NCAyLjUzLTkuMSAyLjVhNzA3LjQyIDcwNy40MiAwIDAgMC00LjQtLjAzbC0zLjI2LS4wMmMtMi4xMyAwLTQuMjUtLjAyLTYuMzgtLjAzdi0uOTdsLS4wMS0uNTVjLjA1LTIuMSAxLjQyLTMuNzcgMi44Ni01LjE2YTcuNTYgNy41NiAwIDAgMSA0LjgtMnoiIGZpbGw9IiNFNjIwNTciLz48cGF0aCBkPSJNNi4zMSAyNS42OGE0Ljk1IDQuOTUgMCAwIDEgMi4yNSAyLjgzYy4yNiAxLjMuMDcgMi41MS0uNiAzLjY1YTQuODQgNC44NCAwIDAgMS0zLjIgMS45MiA0Ljk4IDQuOTggMCAwIDEtMi45NS0uNjhjLS45NC0uODgtMS43Ni0xLjY3LTEuODUtMy0uMDItMS41OS4wNS0yLjUzIDEuMDgtMy43NyAxLjU1LTEuMyAzLjM0LTEuODIgNS4yNy0uOTV6IiBmaWxsPSIjRTUyMDU3Ii8+PC9zdmc+&colorA=FFFFFF)](https://dev.flare.network/)

# Consensus Learning with LLMs

This repository offers a Python implementation of a single-node multi-model Consensus Learning (CL) framework.
CL is a decentralized ensemble learning paradigm introduced in [2402.16157](https://arxiv.org/abs/2402.16157).

The current implementation is a centralized version of CL specialized to Large Language Models (LLMs). This is achieved through OpenAI's [OpenRouter](https://openrouter.ai/docs/quick-start), which provides access to more than 300 models through a unique interface.

This repository serves as a reference point for the Consensus Learning track at the **Verifiable AI Hackathon** organized by Google Cloud x Flare.
For more details about the hackathon tracks we refer to the [main hackathon website](https://hackathon.flare.network/).
Make sure to check [Flare's blogpost](https://flare.network/flare-x-google-cloud-hackathon/) for additional information.

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

### OpenAI API Key

Generate an [OpenRouter API key](https://openrouter.ai/settings/keys) and add it to the `env` variables.
You can check your available credits running:

```bash
uv run python -m tests.credits
```

## OpenRouter Endpoints

You can obtain a list of all models, and a separate list of all *free* models supported by OpenRouter by running:

```bash
uv run python -m tests.models
```

This will generate two `json` files in a `data` folder within the root directory.
To trim this list down to models that work correctly, run:

```bash
uv run python -m tests.working_models
```

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

When running the `default` mode, a set of predefined prompts will be used.
In the `interactive` mode you can manually enter new `user` prompts, with any previous model responses being kept as `assistant` responses.

## Consensus Learning

The current implementation of consensus learning can be described as follows:

1. An initial prompt is send to a set of `N` LLMs.
2. The outputs provided by the `N` LLMs is then sent to a centralized aggregator, which is another LLM with additional context.
3. The centralized LLM aggregates all responses into a single one, which is fed back to the `N` selected models.
4. The process repeats for a number of iterations, which is a configurable parameter, with the last aggregation serving as the final response.

The input parameters for running a single-node multi-model instance of Consensus Learning through OpenRouter are specified within `src/input.json`, as follows:

* Select the `models` by specifying the OpenRouter `id`, as well as some additional LLM-specific parameters such as `max_tokens` and `temperature`.
* Provide an `initial_conversation` for the LLMs, which could include for instance a `system` message and a `user` query prompt.
* Specify the aggregator `model`, additional context `aggregator_context` for the aggregator, as well as a prompt `aggregator_prompt` for how to perform the aggregation.
* Aggregated prompts are resent to models with a role assigned by the `aggregated_prompt_type`.
* This aggregated prompt is sent together with an additional `improvement_prompt` (with predefined `user` role).
* Finally, specify the number of `iterations`.

Once the `src/input.json` file is set, to run the algorithm use:

```bash
uv run python -m src.main
```

## References and Potential Directions

There are various ways in which the current implementation could be improved.

* Mixture-of-Agents (MoA) [github repository](https://github.com/togethercomputer/MoA) and the original paper [arXiv:2406.04692](https://arxiv.org/abs/2406.04692): iterative aggregation of model responses.
* Chain of Thought prompting techniques: a linear problem solving approach where each step builds upon the previous one.
* LLM-Blender introduced in [arXiv:2306.02561](https://arxiv.org/abs/2306.02561): its PairRanker achieves a re-ranking of outputs by performing pairwise comparisons through a *cross-attention encoder* to select the best one.
The best candidates are then concatenated with the initial input.
* Centralized router: another possibility is to train a *router* that predicts the best-performing model from a fixed set of LLMs, for a given input.
See *e.g.* [arXiv:2311.08692](https://arxiv.org/abs/2311.08692), [arXiv:2309:15789](https://arxiv.org/pdf/2309.15789)
