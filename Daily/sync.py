import json
import os
from datetime import datetime
from parsing import parse_markdown  # Ensure this imports correctly

TASKS_FOLDER = os.path.expanduser("~/Notes/Daily")


def save_to_json(year: int, parsed_data):
    """Convert parsed markdown data into JSON format and save."""
    json_file = os.path.join(TASKS_FOLDER, str(year), f"{year}.json")

    all_tasks = []
    for entry in parsed_data:
        for task in entry["tasks"]:
            all_tasks.append(
                {
                    "date": entry["date"],
                    "completed_date": task.get("completed_date", None),
                    "completed": task["completed"],
                    "tag": task.get("tag", ""),
                    "description": task["name"],
                }
            )

    with open(json_file, "w", encoding="utf-8") as json_out:
        json.dump(all_tasks, json_out, indent=4)

    print(f"✅ Synced tasks for {year} into {json_file}")


def sync_year_json(year: int):
    """Sync all .md files for a given year into JSON format."""
    year_folder = os.path.join(TASKS_FOLDER, str(year))

    all_parsed_data = []
    for month in range(1, 13):
        month_name = datetime(year, month, 1).strftime("%B")
        md_file = os.path.join(year_folder, f"{month_name}.md")

        if os.path.exists(md_file):
            parsed_data = parse_markdown(md_file)
            all_parsed_data.extend(parsed_data)

    save_to_json(year, all_parsed_data)
