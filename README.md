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

You can create a `models.json` file with all supported models, saved in a new `data` folder by running:

```bash
uv run python -m tests.models
```
