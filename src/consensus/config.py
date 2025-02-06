from dataclasses import dataclass


@dataclass(frozen=True)
class AggregatorConfig:
    model: str
    approach: str


@dataclass(frozen=True)
class ConsensusConfig:
    models: list[str]
    aggregator: list[AggregatorConfig]
    initial_prompt: list[dict]
    improvement_prompt: str
    iterations: int
    new_prompt_type: str
    max_tokens: int
    temperature: float

    @staticmethod
    def load_parameters(json_data: dict) -> "ConsensusConfig":
        aggregator_configs = [
            AggregatorConfig(**aggr) for aggr in json_data.get("aggregator", [])
        ]
        return ConsensusConfig(
            models=json_data.get("models", []),
            aggregator=aggregator_configs,
            initial_prompt=json_data.get("initial_prompt", []),
            improvement_prompt=json_data.get("improvement_prompt", ""),
            iterations=json_data.get("iterations", 1),
            new_prompt_type=json_data.get("new_prompt_type", "system"),
            max_tokens=json_data.get("max_tokens", 1500),
            temperature=json_data.get("temperature", 0.7),
        )
