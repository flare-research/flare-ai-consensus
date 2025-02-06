import json
from pathlib import Path

def save_json(contents: dict, file_path: Path) -> None:
    """Save json files to specified path."""

    with open(file_path, "w") as f:
        json.dump(contents, f, indent=4)
    print(f"Data saved to {file_path}.")
