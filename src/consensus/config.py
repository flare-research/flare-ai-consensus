from dataclasses import dataclass


@dataclass(frozen=True)
class AggregatorConfig:
    model: str
    approach: str
    context: list[dict]
    prompt: list[dict]


@dataclass(frozen=True)
class ConsensusConfig:
    models: list[str]
    aggregator: AggregatorConfig
    initial_prompt: list[dict]
    improvement_prompt: str
    iterations: int
    aggregated_prompt_type: str
    max_tokens: int
    temperature: float

    @staticmethod
    def load_parameters(json_data: dict) -> "ConsensusConfig":
        aggr = json_data.get("aggregator", [])[0]
        aggregator_configs = AggregatorConfig(
            model=aggr["model"],
            approach=aggr["approach"],
            context=aggr.get("aggregator_context", []),
            prompt=aggr.get("aggregator_prompt", []),
        )
        return ConsensusConfig(
            models=json_data.get("models", []),
            aggregator=aggregator_configs,
            initial_prompt=json_data.get("initial_conversation", []),
            improvement_prompt=json_data.get("improvement_prompt", ""),
            iterations=json_data.get("iterations", 1),
            aggregated_prompt_type=json_data.get("aggregated_prompt_type", "system"),
            max_tokens=json_data.get("max_tokens", 1500),
            temperature=json_data.get("temperature", 0.7),
        )
