import os
import re

from json_handler import save_json
from parsing import parse_markdown
from date_paths import BASE_DIR


def sync_json(file_path):
    """
    Syncs a single Markdown file to JSON.
    """
    json_data = parse_markdown(file_path)
    if not json_data.get("entries"):
        print(f"Warning: No tasks found in {file_path}. JSON will still be updated.")

    json_path = file_path.replace(".md", ".json")
    save_json(json_path, json_data)


def sync_year(year: int):
    """
    Sync all valid Markdown files for the given year into JSON format.
    """
    year_folder = os.path.join(BASE_DIR, str(year))

    if not os.path.exists(year_folder):
        print(f"Warning: No directory found for {year}. Create it first.")
        return

    md_pattern = re.compile(rf"^{year}_(0[1-9]|1[0-2])_[a-z]{{3}}\.md$")
    md_files = [
        os.path.join(year_folder, f)
        for f in os.listdir(year_folder)
        if md_pattern.match(f)
    ]
    if not md_files:
        print(f"No Markdown files found in {year_folder}. Nothing to sync.")
        return

    for file_path in md_files:
        sync_json(file_path)

    print(f"Synced {len(md_files)} Markdown files for {year}.")
