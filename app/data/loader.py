import json
from pathlib import Path


def save_data(filename: str, data) -> bool:
    try:
        file_path = Path(filename)
        if file_path.parent and str(file_path.parent) != ".":
            file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)

        return True
    except (OSError, TypeError, ValueError):
        return False
