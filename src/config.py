import json
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, kw_only=True)
class Config:
    open_router_base_url: str
    open_router_api_key: str
    data_path: Path
    input_path: Path


def load_env_var(var_name: str) -> str:
    """Loads and validates environment variables."""
    return os.getenv(var_name, default="")


def create_path(folder_name: str) -> Path:
    """Creates and returns a path for storing data or logs."""
    path = Path(__file__).parent.resolve().parent / f"{folder_name}"
    path.mkdir(exist_ok=True)
    return path


# Initialize configuration
config = Config(
    open_router_base_url=load_env_var("OPENROUTER_BASE_URL"),
    open_router_api_key=load_env_var("OPENROUTER_API_KEY"),
    data_path=create_path("data"),
    input_path=create_path("src"),
)
