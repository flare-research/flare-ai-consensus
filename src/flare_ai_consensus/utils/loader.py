import json
from pathlib import Path


def load_txt(file_path: Path) -> str:
    """Load a txt file from a specified path."""
    with file_path.open() as f:
        return f.read().strip()


def load_json(file_path: Path) -> dict:
    """Read the selected model IDs from a JSON file."""
    with file_path.open() as f:
        return json.load(f)
