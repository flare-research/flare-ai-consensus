from dataclasses import dataclass
from typing import Literal

from flare_ai_consensus.router import Message


@dataclass(frozen=True)
class ModelConfig:
    model_id: str
    max_tokens: int = 50
    temperature: float = 0.7


@dataclass(frozen=True)
class AggregatorConfig:
    model: ModelConfig
    approach: str
    context: list[Message]
    prompt: list[Message]


@dataclass(frozen=True)
class ConsensusConfig:
    models: list[ModelConfig]
    aggregator_config: AggregatorConfig
    initial_prompt: list[Message]
    improvement_prompt: str
    iterations: int
    aggregated_prompt_type: Literal["user", "assistant", "system"]

    @staticmethod
    def load_parameters(json_data: dict) -> "ConsensusConfig":
        # Parse the list of models.
        models = [
            ModelConfig(
                model_id=m["id"],
                max_tokens=m["max_tokens"],
                temperature=m["temperature"],
            )
            for m in json_data.get("models", [])
        ]

        # Parse the aggregator configuration.
        aggr_data = json_data.get("aggregator", [])[0]
        aggr_model_data = aggr_data.get("model", {})
        aggregator_model = ModelConfig(
            model_id=aggr_model_data["id"],
            max_tokens=aggr_model_data["max_tokens"],
            temperature=aggr_model_data["temperature"],
        )
        aggregator_config = AggregatorConfig(
            model=aggregator_model,
            approach=aggr_data.get("approach", ""),
            context=aggr_data.get("aggregator_context", []),
            prompt=aggr_data.get("aggregator_prompt", []),
        )

        # Set up the initial_prompt.
        initial_prompt = json_data.get("initial_conversation", [])

        return ConsensusConfig(
            models=models,
            aggregator_config=aggregator_config,
            initial_prompt=initial_prompt,
            improvement_prompt=json_data.get("improvement_prompt", ""),
            iterations=json_data.get("iterations", 1),
            aggregated_prompt_type=json_data.get("aggregated_prompt_type", "system"),
        )
