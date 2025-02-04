import json
import os


def load_json(file_path: str) -> list:
    """
    Load a JSON file and return its content as a list. If the file doesn't exist or is invalid, return an empty list.
    """
    if not os.path.exists(file_path):
        print(f"WARNING: {file_path} does not exist.")
        return []
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON format in {file_path}. Returning empty list.")
        return []


def save_json(file_path: str, data: list) -> None:
    """
    Save tasks to a JSON file.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    print(f"✅ JSON saved: {file_path}")
