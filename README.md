[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
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
uv run pyright
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
Note that free models are subject to the following rate limits:

* 20 requests per minute.
* 200 requests per day.

All models should function correctly, in principle, but some models may return errors.
If you wish to trim the list of free models down to working models, you can run the `tests/working_models.py` script.
Note, however, that this will bring you closer to the daily rate limit on the free models since there are around 27 models listed as free.

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
To exit the `interactive` mode simply write `exit`.

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
uv run start-consensus
```

## References and Potential Directions

The primary consideration is how the ensemble of LLMs will be integrated and utilized.
A key requirement for the hackathon is that the code must run within a trusted execution environment (TEE), ensuring confidentiality and integrity while interacting with Flare's blockchain.

An essential part of the design process is defining a clear **use case**.
Participants should carefully consider how the algorithm will be used, ensuring that it aligns with the security guarantees of a TEE and the constraints of blockchain interactions.
This includes evaluating the types of inputs received, potential risks associated with on-chain data, and how the model's outputs will be consumed.
Designing with a well-defined use case in mind will ensure that the solution is both practical and secure within the given environment.

For the consensus learning algorithm itself, there are various ways in which the current implementation could be improved.
Some useful references and potential ideas include:

* **Factual correctness**:
  * In line with the main theme of the hackathon, one important aspect of the outputs generated by the LLMs is their accuracy. In this regard, producing sources/citations with the answers would lead to higher trust in the setup. Sample prompts that can be used for this purpose can be found in the appendices of [arXiv:2305.14627](https://arxiv.org/pdf/2305.14627), or in [James' Coffee Blog](https://jamesg.blog/2023/04/02/llm-prompts-source-attribution).
  * *Note*: only certain models may be suitable for this purpose, as references generated by LLMs are often inaccurate or not even real!
* **Prompt engineering**:
  * Our approach is very similar to the **Mixture-of-Agents (MoA)** introduced in [arXiv:2406.04692](https://arxiv.org/abs/2406.04692), which uses iterative aggregations of model responses. Ther [github repository](https://github.com/togethercomputer/MoA) does include other examples of prompts that can be used for additional context for the LLMs.
  * New iterations of the consensus learning algorithm could have different prompts for improving the previous responses. In this regard, the *few-shot* prompting techniques introduced by OpenAI in [arXiv:2005.14165](https://arxiv.org/pdf/2005.14165) work by providing models with a *few* examples of similar queries and responses in addition to the initial prompt. (See also previous work by [Radford et al.](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf).)
  * *Chain of Thought* prompting techniques are a linear problem solving approach where each step builds upon the previous one. Google's approach in [arXiv:2201.11903](https://arxiv.org/pdf/2201.11903) is to augment each prompt with an additional example and chain of thought for an associated answer. (See the paper for multiple examples.)
* **Dynamic resource allocation**:
  * An immediate improvement to the current approach would be to use dynamically-adjusted parameters. Namely, the number of iterations and number of models used in the algorithm could be adjusted to the input prompt: *e.g.* simple prompts do not require too many resources. For this, a centralized model could be used to decide the complexity of the task, prior to sending the prompt to the other LLMs.
  * On a similar note, the number of iterations for making progress could adjusted according to how *different* are the model responses. While semantic entailment for LLM outputs is a notoriously difficult topic, the use of [LLM-as-a-Judge](https://arxiv.org/pdf/2306.05685) for evaluating other LLM outputs has shown good progress -- see also this [Confident AI blogpost](https://www.confident-ai.com/blog/why-llm-as-a-judge-is-the-best-llm-evaluation-method).
* **Semantic filters**:
  * In line with the previously mentioned LLM-as-a-Judge, a model could potentially be used for filtering *bad* responses.
  * LLM-Blender, for instance, introduced in [arXiv:2306.02561](https://arxiv.org/abs/2306.02561), uses a PairRanker that achieves a ranking of outputs through pairwise comparisons via a *cross-attention encoder*.
* **AI Agent Swarm**:
  * The structure of the reference CL implementation can be changed to adapt *swarm*-type algorithms, where tasks are broken down and distributed among specialized agents for parallel processing. In this case a centralized LLM would act as an orchestrator for managing distribution of tasks -- see *e.g.* [swarms repo](https://github.com/kyegomez/swarms?source=post_page-----c554f5be421b--------------------------------).