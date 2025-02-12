import json
from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)


def save_json(contents: dict, file_path: Path) -> None:
    """Save json files to specified path."""

    with file_path.open("w") as f:
        json.dump(contents, f, indent=4)
    logger.info("saved data", file_path=file_path)
