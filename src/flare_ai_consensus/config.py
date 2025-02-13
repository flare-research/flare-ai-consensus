from pathlib import Path

import structlog
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = structlog.get_logger(__name__)
import structlog
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = structlog.get_logger(__name__)


def create_path(folder_name: str) -> Path:
    """Creates and returns a path for storing data or logs."""
    path = Path(__file__).parent.resolve().parent / f"{folder_name}"
    path.mkdir(exist_ok=True)
    return path


class Config(BaseSettings):
    """
    Application settings model that provides configuration for all components.
    """

    # Base URL for OpenRouter
    open_router_base_url: str = "https://openrouter.ai/api/v1"
    # API Key for OpenRouter
    open_router_api_key: str = ""
    # Path to save final data
    data_path: Path = create_path("data")
    # Input path for loading JSON
    input_path: Path = create_path("flare_ai_consensus")

    model_config = SettingsConfigDict(
        # This enables .env file support
        env_file=".env",
        # If .env file is not found, don't raise an error
        env_file_encoding="utf-8",
        # Optional: you can also specify multiple .env files
        extra="ignore",
    )


# Create a global settings instance
config = Config()
logger.debug("config", settings=config.model_dump())
