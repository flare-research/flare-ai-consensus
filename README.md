[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Flare](https://img.shields.io/badge/flare-network-e62058.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNCIgaGVpZ2h0PSIzNCI+PHBhdGggZD0iTTkuNC0uMWEzMjAuMzUgMzIwLjM1IDAgMCAwIDIuOTkuMDJoMi4yOGExMTA2LjAxIDExMDYuMDEgMCAwIDEgOS4yMy4wNGMzLjM3IDAgNi43My4wMiAxMC4xLjA0di44N2wuMDEuNDljLS4wNSAyLTEuNDMgMy45LTIuOCA1LjI1YTkuNDMgOS40MyAwIDAgMS02IDIuMDdIMjAuOTJsLTIuMjItLjAxYTQxNjEuNTcgNDE2MS41NyAwIDAgMS04LjkyIDBMMCA4LjY0YTIzNy4zIDIzNy4zIDAgMCAxLS4wMS0xLjUxQy4wMyA1LjI2IDEuMTkgMy41NiAyLjQgMi4yIDQuNDcuMzcgNi43LS4xMiA5LjQxLS4wOXoiIGZpbGw9IiNFNTIwNTgiLz48cGF0aCBkPSJNNy42NSAxMi42NUg5LjJhNzU5LjQ4IDc1OS40OCAwIDAgMSA2LjM3LjAxaDMuMzdsNi42MS4wMWE4LjU0IDguNTQgMCAwIDEtMi40MSA2LjI0Yy0yLjY5IDIuNDktNS42NCAyLjUzLTkuMSAyLjVhNzA3LjQyIDcwNy40MiAwIDAgMC00LjQtLjAzbC0zLjI2LS4wMmMtMi4xMyAwLTQuMjUtLjAyLTYuMzgtLjAzdi0uOTdsLS4wMS0uNTVjLjA1LTIuMSAxLjQyLTMuNzcgMi44Ni01LjE2YTcuNTYgNy41NiAwIDAgMSA0LjgtMnoiIGZpbGw9IiNFNjIwNTciLz48cGF0aCBkPSJNNi4zMSAyNS42OGE0Ljk1IDQuOTUgMCAwIDEgMi4yNSAyLjgzYy4yNiAxLjMuMDcgMi41MS0uNiAzLjY1YTQuODQgNC44NCAwIDAgMS0zLjIgMS45MiA0Ljk4IDQuOTggMCAwIDEtMi45NS0uNjhjLS45NC0uODgtMS43Ni0xLjY3LTEuODUtMy0uMDItMS41OS4wNS0yLjUzIDEuMDgtMy43NyAxLjU1LTEuMyAzLjM0LTEuODIgNS4yNy0uOTV6IiBmaWxsPSIjRTUyMDU3Ii8+PC9zdmc+&colorA=FFFFFF)](https://dev.flare.network/)

# Flare AI Consensus

Flare AI SDK for Consensus Learning.

This repository provides a Python implementation of a single-node, multi-model **Consensus Learning (CL)** framework. CL is a decentralized ensemble learning approach described in [arXiv:2402.16157](https://arxiv.org/abs/2402.16157).

The current implementation specializes in leveraging Large Language Models (LLMs) through a centralized architecture using OpenAI's [OpenRouter](https://openrouter.ai/docs/quick-start). OpenRouter offers access to over 300 models via a unified interface.

This repository serves as the reference implementation for the **Consensus Learning track** at the **Verifiable AI Hackathon** organized by Google Cloud in collaboration with Flare. For more details, please visit the [main hackathon website](https://hackathon.flare.network/) and [Flare’s blogpost](https://flare.network/flare-x-google-cloud-hackathon/).

## 🚀 Key Features

- **Consensus Learning:** Provides a Python implementation of a single-node, multi-model of Consensus Learning, a decentralized ensemble learning approach described in [arXiv:2402.16157](https://arxiv.org/abs/2402.16157).
- **Over 300 models supported:** Leverages LLMs via a centralized architecture using OpenAI's [OpenRouter](https://openrouter.ai/docs/quick-start).

## Prerequisites

Install all dependencies using [uv](https://docs.astral.sh/uv/getting-started/installation/) by running:

```bash
uv sync --all-extras
```

### OpenAI API Key

Generate an [OpenRouter API key](https://openrouter.ai/settings/keys) and set it in your environment variables. You can verify your available credits by running:

```bash
uv run python -m tests.credits
```

## OpenRouter Endpoints

The repository provides scripts to interact with OpenRouter:

- **List All Models:**  
  Retrieves a list of all models.
- **List Free Models:**  
  Retrieves a list of all free models supported by OpenRouter.

Run the following command to generate two JSON files in the `data` folder:

```bash
uv run python -m tests.models
```

**Note:**  
Free models are limited to 20 requests per minute and 200 requests per day.
Although all models should work in principle, some may return errors. To filter down to working free models, run:

```bash
uv run python -m tests.working_models
```

## Consensus Learning Workflow

The consensus learning algorithm operates as follows:

1. **Initial Prompt:**  
   An initial prompt is sent to a set of `N` LLMs.
2. **Aggregation:**  
   The outputs from these models are collected and sent to a centralized aggregator LLM, along with additional context.
3. **Feedback Loop:**  
   The aggregator compiles a single, refined response which is then fed back to the `N` models.
4. **Iteration:**  
   This process is repeated for a configurable number of iterations. The final aggregated response is returned as the result.

### Input Configuration

All input parameters for running the consensus learning instance are specified in `src/input.json`:

- **Models:**  
  Select the LLMs by specifying their OpenRouter `id` along with parameters such as `max_tokens` and `temperature`.
- **Initial Conversation:**  
  Provide the conversation context (e.g., a `system` message and an initial `user` query).
- **Aggregator Configuration:**  
  Define the aggregator model, additional context (`aggregator_context`), and the prompt (`aggregator_prompt`) for how aggregation should occur.
- **Aggregated Prompt Type:**  
  Specify how the aggregated prompt should be treated when re-sent to the models.
- **Improvement Prompt:**  
  Include an additional prompt (`improvement_prompt`) to further refine responses.
- **Iterations:**  
  Set the number of iterations for the consensus process.

## Running the Consensus Learning Algorithm

Once you have configured `src/input.json`, start the consensus learning process by running:

```bash
uv run start-consensus
```

Additionally, you can test the individual endpoints:

- **Completion Endpoint:**  
  Generate a text completion (non-conversational):

  ```bash
  uv run python -m tests.completion --prompt "Who is Ash Ketchum?" --model "google/learnlm-1.5-pro-experimental:free"
  ```

- **Chat Completion Endpoint:**  
  Test the conversational mode with history tracking:

  ```bash
  uv run python -m tests.chat_completion --mode default
  ```

  In `interactive` mode, you can enter new `user` prompts manually. Type `exit` to leave interactive mode.

## References and Future Directions

### Key Considerations

- **Security & TEE:**  
  The solution must run within a Trusted Execution Environment (TEE) to ensure confidentiality and integrity, especially when interacting with Flare's blockchain.
- **Use Case Definition:**  
  Clearly define how the consensus learning algorithm will be used and ensure it aligns with security guarantees and blockchain constraints.

### Potential Improvements

- **Factual Accuracy:**  
  Enhance response accuracy by generating sources or citations. Check out strategies in [arXiv:2305.14627](https://arxiv.org/pdf/2305.14627) or [James' Coffee Blog](https://jamesg.blog/2023/04/02/llm-prompts-source-attribution).  
  _Note:_ Some models may generate inaccurate references.

- **Prompt Engineering:**  
  Experiment with different prompt designs. Our approach is similar to the **Mixture-of-Agents (MoA)** from [arXiv:2406.04692](https://arxiv.org/abs/2406.04692). Refer to the [MoA GitHub repository](https://github.com/togethercomputer/MoA) for further examples.  
  Techniques like _few-shot_ prompting ([arXiv:2005.14165](https://arxiv.org/pdf/2005.14165)) and _Chain of Thought_ ([arXiv:2201.11903](https://arxiv.org/pdf/2201.11903)) can also be explored.

- **Dynamic Resource Allocation:**  
  Consider adjusting the number of iterations or models based on prompt complexity. A centralized model could determine task complexity before dispatching requests to other LLMs.  
  Additionally, use methods like [LLM-as-a-Judge](https://arxiv.org/pdf/2306.05685) for evaluating response quality.

- **Semantic Filters:**  
  Implement semantic filters using techniques such as the PairRanker from [LLM-Blender](https://arxiv.org/abs/2306.02561) to filter out low-quality responses.

- **AI Agent Swarm:**  
  Explore swarm-type architectures where tasks are distributed among specialized agents, with a centralized LLM orchestrating the process. See the [Swarms repository](https://github.com/kyegomez/swarms?source=post_page-----c554f5be421b--------------------------------) for inspiration.
