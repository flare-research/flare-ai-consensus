from pathlib import Path
from typing import Literal, TypedDict

import structlog
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = structlog.get_logger(__name__)


def create_path(folder_name: str) -> Path:
    """Creates and returns a path for storing data or logs."""
    path = Path(__file__).parent.resolve().parent / f"{folder_name}"
    path.mkdir(exist_ok=True)
    return path


class Message(TypedDict):
    role: str
    content: str


class ModelConfig(BaseModel):
    """Configuration for individual models"""

    model_id: str
    max_tokens: int = 50
    temperature: float = 0.7


class AggregatorConfig(BaseModel):
    """Configuration for the aggregator"""

    model: ModelConfig
    approach: str
    context: list[Message]
    prompt: list[Message]


class ConsensusConfig(BaseModel):
    """Configuration for the consensus mechanism"""

    models: list[ModelConfig]
    aggregator_config: AggregatorConfig
    improvement_prompt: str
    iterations: int
    aggregated_prompt_type: Literal["user", "assistant", "system"]

    @classmethod
    def from_json(cls, json_data: dict) -> "ConsensusConfig":
        """Create ConsensusConfig from JSON data"""
        # Parse the list of models
        models = [
            ModelConfig(
                model_id=m["id"],
                max_tokens=m["max_tokens"],
                temperature=m["temperature"],
            )
            for m in json_data.get("models", [])
        ]

        # Parse the aggregator configuration
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

        return cls(
            models=models,
            aggregator_config=aggregator_config,
            improvement_prompt=json_data.get("improvement_prompt", ""),
            iterations=json_data.get("iterations", 1),
            aggregated_prompt_type=json_data.get("aggregated_prompt_type", "system"),
        )


class Settings(BaseSettings):
    """
    Application settings model that provides configuration for all components.
    Combines both infrastructure and consensus settings.
    """

    # OpenRouter Settings
    open_router_base_url: str = "https://openrouter.ai/api/v1"
    open_router_api_key: str = ""

    # Path Settings
    data_path: Path = create_path("data")
    input_path: Path = create_path("flare_ai_consensus")

    # Restrict backend listener to specific IPs
    cors_origins: list[str] = ["*"]

    # Consensus Settings
    consensus_config: ConsensusConfig | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def load_consensus_config(self, json_data: dict) -> None:
        """Load consensus configuration from JSON data"""
        self.consensus_config = ConsensusConfig.from_json(json_data)
        logger.info("loaded consensus configuration")


# Create a global settings instance
settings = Settings()
logger.debug("settings initialized", settings=settings.model_dump())
