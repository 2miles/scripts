import json
import os


def load_json(file_path: str) -> dict:
    """
    Load a JSON file and return its content as a dictionary.
    If the file doesn't exist or is invalid, return an empty dictionary.
    """
    if not os.path.exists(file_path):
        return {"entries": []}

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {"entries": []}
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON format in {file_path}. Returning empty dictionary.")
        return {"entries": []}


def save_json(file_path: str, data: dict) -> None:
    """
    Save structured data to a JSON file.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
