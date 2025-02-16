import json
from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)


def load_txt(file_path: Path) -> str:
    """Load a txt file from a specified path."""
    with file_path.open() as f:
        return f.read().strip()


def load_json(file_path: Path) -> dict:
    """Read the selected model IDs from a JSON file."""
    with file_path.open() as f:
        return json.load(f)


def save_json(contents: dict, file_path: Path) -> None:
    """Save json files to specified path."""

    with file_path.open("w") as f:
        json.dump(contents, f, indent=4)
    logger.info("saved data", file_path=file_path)
