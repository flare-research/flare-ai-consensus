[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Flare](https://img.shields.io/badge/flare-network-e62058.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNCIgaGVpZ2h0PSIzNCI+PHBhdGggZD0iTTkuNC0uMWEzMjAuMzUgMzIwLjM1IDAgMCAwIDIuOTkuMDJoMi4yOGExMTA2LjAxIDExMDYuMDEgMCAwIDEgOS4yMy4wNGMzLjM3IDAgNi43My4wMiAxMC4xLjA0di44N2wuMDEuNDljLS4wNSAyLTEuNDMgMy45LTIuOCA1LjI1YTkuNDMgOS40MyAwIDAgMS02IDIuMDdIMjAuOTJsLTIuMjItLjAxYTQxNjEuNTcgNDE2MS41NyAwIDAgMS04LjkyIDBMMCA4LjY0YTIzNy4zIDIzNy4zIDAgMCAxLS4wMS0xLjUxQy4wMyA1LjI2IDEuMTkgMy41NiAyLjQgMi4yIDQuNDcuMzcgNi43LS4xMiA5LjQxLS4wOXoiIGZpbGw9IiNFNTIwNTgiLz48cGF0aCBkPSJNNy42NSAxMi42NUg5LjJhNzU5LjQ4IDc1OS40OCAwIDAgMSA2LjM3LjAxaDMuMzdsNi42MS4wMWE4LjU0IDguNTQgMCAwIDEtMi40MSA2LjI0Yy0yLjY5IDIuNDktNS42NCAyLjUzLTkuMSAyLjVhNzA3LjQyIDcwNy40MiAwIDAgMC00LjQtLjAzbC0zLjI2LS4wMmMtMi4xMyAwLTQuMjUtLjAyLTYuMzgtLjAzdi0uOTdsLS4wMS0uNTVjLjA1LTIuMSAxLjQyLTMuNzcgMi44Ni01LjE2YTcuNTYgNy41NiAwIDAgMSA0LjgtMnoiIGZpbGw9IiNFNjIwNTciLz48cGF0aCBkPSJNNi4zMSAyNS42OGE0Ljk1IDQuOTUgMCAwIDEgMi4yNSAyLjgzYy4yNiAxLjMuMDcgMi41MS0uNiAzLjY1YTQuODQgNC44NCAwIDAgMS0zLjIgMS45MiA0Ljk4IDQuOTggMCAwIDEtMi45NS0uNjhjLS45NC0uODgtMS43Ni0xLjY3LTEuODUtMy0uMDItMS41OS4wNS0yLjUzIDEuMDgtMy43NyAxLjU1LTEuMyAzLjM0LTEuODIgNS4yNy0uOTV6IiBmaWxsPSIjRTUyMDU3Ii8+PC9zdmc+&colorA=FFFFFF)](https://dev.flare.network/)

# Flare AI Consensus

Flare AI SDK for Consensus Learning.

### 🚀 Key Features

- **Consensus Learning Implementation**
  A Python implementation of single-node, multi-model Consensus Learning (CL). CL is a decentralized ensemble learning paradigm introduced in [arXiv:2402.16157](https://arxiv.org/abs/2402.16157).

- **300+ LLM Support**
  Leverages OpenRouter to access over 300 models via a unified interface.

- **Iterative Feedback Loop**
  Employs an aggregation process where multiple LLM outputs are refined over configurable iterations.

- **Modular & Configurable**
  Easily customize models, conversation prompts, and aggregation parameters through a simple JSON configuration.

## 📌 Prerequisites

Before getting started, ensure you have:

- A **Python 3.12** environment.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed for dependency management.
- An [OpenRouter API Key](https://openrouter.ai/settings/keys).

## ⚙️ Environment Setup

### Step 1: Install Dependencies

Install all required dependencies by running:

```bash
uv sync --all-extras
```

### Step 2: Configure Environment Variables

Rename `.env.example` to `.env` and add in the variables (e.g. your [OpenRouter API Key](https://openrouter.ai/keys))

Verify your available credits and get all supported models with:

```bash
uv run python -m tests.credits
uv run python -m tests.models
```

## 🚀 Running Consensus Learning

Configure your consensus learning instance in `src/input.json`, including:

- **Models:**
  Specify each LLM's OpenRouter `id`, along with parameters like `max_tokens` and `temperature`.

- **Initial Conversation:**
  Set up the conversation context (e.g., a `system` message and an initial `user` query).

- **Aggregator Settings:**
  Define the aggregator model, additional context, aggregation prompt, and specify how aggregated responses are handled.

- **Iterations:**
  Determine the number of iterations for the feedback loop.

Once configured, start the process with:

```bash
uv run start-consensus
```

## 🔧 Testing Endpoints

For granular testing, use the following endpoints:

- **Completion Endpoint (Non-Conversational):**

  ```bash
  uv run python -m tests.completion --prompt "Who is Ash Ketchum?" --model "google/learnlm-1.5-pro-experimental:free"
  ```

- **Chat Completion Endpoint (Conversational):**

  ```bash
  uv run python -m tests.chat_completion --mode default
  ```

  _Tip:_ In interactive mode, type `exit` to quit.

## 🚀 Deploy on TEE

Deploy on a [Confidential Space](https://cloud.google.com/confidential-computing/confidential-space/docs/confidential-space-overview) using AMD SEV.

### Prerequisites

- **Google Cloud Platform Account:**  
  Access to the [`verifiable-ai-hackathon`](https://console.cloud.google.com/welcome?project=verifiable-ai-hackathon) project is required.

- **OpenRouter API Key:**  
  Ensure your [OpenRouter API key](https://openrouter.ai/settings/keys) is in your `.env`.

- **gcloud CLI:**  
  Install and authenticate the [gcloud CLI](https://cloud.google.com/sdk/docs/install).

### Environment Configuration

1. **Set Environment Variables:**  
   Update your `.env` file with:

   ```bash
   TEE_IMAGE_REFERENCE=ghcr.io/flare-research/flare-ai-consensus:main  # Replace with your repo build image
   INSTANCE_NAME=<PROJECT_NAME-TEAM_NAME>
   ```

2. **Load Environment Variables:**

   ```bash
   source .env
   ```

   > **Reminder:** Run the above command in every new shell session. On Windows, we recommend using [git BASH](https://gitforwindows.org) to access commands like `source`.

3. **Verify the Setup:**

   ```bash
   echo $TEE_IMAGE_REFERENCE # Expected output: Your repo build image
   ```

### Deploying to Confidential Space

Run the following command:

```bash
gcloud compute instances create $INSTANCE_NAME \
  --project=verifiable-ai-hackathon \
  --zone=us-central1-d \
  --machine-type=n2d-standard-2 \
  --network-interface=network-tier=PREMIUM,nic-type=GVNIC,stack-type=IPV4_ONLY,subnet=default \
  --metadata=tee-image-reference=$TEE_IMAGE_REFERENCE,\
tee-container-log-redirect=true,\
tee-env-OPEN_ROUTER_API_KEY=$OPEN_ROUTER_API_KEY,\
  --maintenance-policy=MIGRATE \
  --provisioning-model=STANDARD \
  --service-account=confidential-sa@verifiable-ai-hackathon.iam.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --min-cpu-platform="AMD Milan" \
  --tags=flare-ai,http-server,https-server \
  --create-disk=auto-delete=yes,\
boot=yes,\
device-name=$INSTANCE_NAME,\
image=projects/confidential-space-images/global/images/confidential-space-debug-250100,\
mode=rw,\
size=11,\
type=pd-standard \
  --shielded-secure-boot \
  --shielded-vtpm \
  --shielded-integrity-monitoring \
  --reservation-affinity=any \
  --confidential-compute-type=SEV
```

#### Post-deployment

After deployment, you should see an output similar to:

```plaintext
NAME          ZONE           MACHINE_TYPE    PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP    STATUS
consensus-team1   us-central1-d  n2d-standard-2               10.128.0.18  34.41.127.200  RUNNING
```

It may take a few minutes for Confidential Space to complete startup checks.
You can monitor progress via the [GCP Console](https://console.cloud.google.com/welcome?project=verifiable-ai-hackathon) by clicking **Serial port 1 (console)**.
When you see a message like:

```plaintext
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

the container is ready. Navigate to the external IP of the instance (visible in the GCP Console) to access the Chat UI.

### 🔧 Troubleshooting

If you encounter issues, follow these steps:

1. **Check Logs:**

   ```bash
   gcloud compute instances get-serial-port-output $INSTANCE_NAME --project=verifiable-ai-hackathon
   ```

2. **Verify API Key(s):**  
   Ensure that all API Keys are set correctly (e.g. `OPEN_ROUTER_API_KEY`).

3. **Check Firewall Settings:**  
   Confirm that your instance is publicly accessible on port `80`.

## 🔜 Next Steps & Future Directions

- **Security & TEE Integration:**
  - Ensure execution within a Trusted Execution Environment (TEE) to maintain confidentiality and integrity.
- **Factual correctness**:
  - In line with the main theme of the hackathon, one important aspect of the outputs generated by the LLMs is their accuracy. In this regard, producing sources/citations with the answers would lead to higher trust in the setup. Sample prompts that can be used for this purpose can be found in the appendices of [arXiv:2305.14627](https://arxiv.org/pdf/2305.14627), or in [James' Coffee Blog](https://jamesg.blog/2023/04/02/llm-prompts-source-attribution).
  - _Note_: only certain models may be suitable for this purpose, as references generated by LLMs are often inaccurate or not even real!
- **Prompt engineering**:
  - Our approach is very similar to the **Mixture-of-Agents (MoA)** introduced in [arXiv:2406.04692](https://arxiv.org/abs/2406.04692), which uses iterative aggregations of model responses. Ther [github repository](https://github.com/togethercomputer/MoA) does include other examples of prompts that can be used for additional context for the LLMs.
  - New iterations of the consensus learning algorithm could have different prompts for improving the previous responses. In this regard, the _few-shot_ prompting techniques introduced by OpenAI in [arXiv:2005.14165](https://arxiv.org/pdf/2005.14165) work by providing models with a _few_ examples of similar queries and responses in addition to the initial prompt. (See also previous work by [Radford et al.](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf).)
  - _Chain of Thought_ prompting techniques are a linear problem solving approach where each step builds upon the previous one. Google's approach in [arXiv:2201.11903](https://arxiv.org/pdf/2201.11903) is to augment each prompt with an additional example and chain of thought for an associated answer. (See the paper for multiple examples.)
- **Dynamic resource allocation**:
  - An immediate improvement to the current approach would be to use dynamically-adjusted parameters. Namely, the number of iterations and number of models used in the algorithm could be adjusted to the input prompt: _e.g._ simple prompts do not require too many resources. For this, a centralized model could be used to decide the complexity of the task, prior to sending the prompt to the other LLMs.
  - On a similar note, the number of iterations for making progress could adjusted according to how _different_ are the model responses. While semantic entailment for LLM outputs is a notoriously difficult topic, the use of [LLM-as-a-Judge](https://arxiv.org/pdf/2306.05685) for evaluating other LLM outputs has shown good progress -- see also this [Confident AI blogpost](https://www.confident-ai.com/blog/why-llm-as-a-judge-is-the-best-llm-evaluation-method).
- **Semantic filters**:
  - In line with the previously mentioned LLM-as-a-Judge, a model could potentially be used for filtering _bad_ responses.
  - LLM-Blender, for instance, introduced in [arXiv:2306.02561](https://arxiv.org/abs/2306.02561), uses a PairRanker that achieves a ranking of outputs through pairwise comparisons via a _cross-attention encoder_.
- **AI Agent Swarm**:
  - The structure of the reference CL implementation can be changed to adapt _swarm_-type algorithms, where tasks are broken down and distributed among specialized agents for parallel processing. In this case a centralized LLM would act as an orchestrator for managing distribution of tasks -- see _e.g._ [swarms repo](https://github.com/kyegomez/swarms).
