[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Flare](https://img.shields.io/badge/flare-network-e62058.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNCIgaGVpZ2h0PSIzNCI+PHBhdGggZD0iTTkuNC0uMWEzMjAuMzUgMzIwLjM1IDAgMCAwIDIuOTkuMDJoMi4yOGExMTA2LjAxIDExMDYuMDEgMCAwIDEgOS4yMy4wNGMzLjM3IDAgNi43My4wMiAxMC4xLjA0di44N2wuMDEuNDljLS4wNSAyLTEuNDMgMy45LTIuOCA1LjI1YTkuNDMgOS40MyAwIDAgMS02IDIuMDdIMjAuOTJsLTIuMjItLjAxYTQxNjEuNTcgNDE2MS41NyAwIDAgMS04LjkyIDBMMCA4LjY0YTIzNy4zIDIzNy4zIDAgMCAxLS4wMS0xLjUxQy4wMyA1LjI2IDEuMTkgMy41NiAyLjQgMi4yIDQuNDcuMzcgNi43LS4xMiA5LjQxLS4wOXoiIGZpbGw9IiNFNTIwNTgiLz48cGF0aCBkPSJNNy42NSAxMi42NUg5LjJhNzU5LjQ4IDc1OS40OCAwIDAgMSA2LjM3LjAxaDMuMzdsNi42MS4wMWE4LjU0IDguNTQgMCAwIDEtMi40MSA2LjI0Yy0yLjY5IDIuNDktNS42NCAyLjUzLTkuMSAyLjVhNzA3LjQyIDcwNy40MiAwIDAgMC00LjQtLjAzbC0zLjI2LS4wMmMtMi4xMyAwLTQuMjUtLjAyLTYuMzgtLjAzdi0uOTdsLS4wMS0uNTVjLjA1LTIuMSAxLjQyLTMuNzcgMi44Ni01LjE2YTcuNTYgNy41NiAwIDAgMSA0LjgtMnoiIGZpbGw9IiNFNjIwNTciLz48cGF0aCBkPSJNNi4zMSAyNS42OGE0Ljk1IDQuOTUgMCAwIDEgMi4yNSAyLjgzYy4yNiAxLjMuMDcgMi41MS0uNiAzLjY1YTQuODQgNC44NCAwIDAgMS0zLjIgMS45MiA0Ljk4IDQuOTggMCAwIDEtMi45NS0uNjhjLS45NC0uODgtMS43Ni0xLjY3LTEuODUtMy0uMDItMS41OS4wNS0yLjUzIDEuMDgtMy43NyAxLjU1LTEuMyAzLjM0LTEuODIgNS4yNy0uOTV6IiBmaWxsPSIjRTUyMDU3Ii8+PC9zdmc+&colorA=FFFFFF)](https://dev.flare.network/)

# Consensus Learning with LLMs

## OpenRouter Clients

We implement two OpenRouter clients for interacting with the OpenRouter API: a standard sync client and an asynchronous client.
Both of these are constructed on top of some base client (`BaseClient` and `AsyncBaseClient`, respectively) which includes simple logic for API interaction.
Namely, the base clients introduce the `get` and `post` requests.

The `OpenRouterClient` (and `AsyncOpenRouterClient`) build on these base clients by providing specific API endpoints for interacting with the OpenRouter API.

## Messaging

Messages sent to the LLMs are built and within `src/consensus`.
Standard (*i.e.* non-aggregated) messages are sent using the `send_round()` method within `consensus/consensus.py`:

* Initial messages (first round messages) consist of the `initial_conversation` defined within `input.json`.
* Follow-up conversations are built using the `build_improvement_conversation()` method and contain the following:
  * The initial conversation defined within `input.json`.
  * The aggregated prompt from the aggregator, with the role assigned in the `aggregated_prompt_type` field of `input.json`.
  * The `improvement_prompt` defined in `input.json`, which is assigned a `user` role.

## Aggregator

The simplest aggregation method does not rely on an LLM, and instead does a simple concatenation of multiple responses.
For this one can use the `concatenate_aggregator()` method of `consensus/aggregator.py`.

The `centralized_llm_aggregator()` method relies on a specified model to which the individual responses are sent to.
The prompt is built as follows:

* A first message defined in the `aggregator_context` field of the `input.json`.
* A `system` message containing all responses from the contributing LLMs, concatenated together.
* A `user` message defined in the `aggregator_prompt` field of the `input.json`.

## Config

The data from the `input.json` is loaded into a set of classes, defined within `consensus/config.py`:

* `ModelConfig`: a class for specifying an LLM.
* `AggregatorConfig`: a class dedicated to the aggregator model.
* `ConsensusConfig`: the main class used for loading the input data.
