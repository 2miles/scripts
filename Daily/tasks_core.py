import os
import re
from typing import Dict, List

from tasks_printers import print_unfinished_tasks
from parsing import write_markdown
from json_handler import load_json, save_json
from date_paths import (
    get_current_date,
    get_current_date_day,
    get_file_path,
    get_json_file_path,
    get_prev_json_file_path,
)


def create_new_day(data: Dict[str, List[Dict]], date: str) -> Dict:
    """
    Ensure today's section exists in the data.
    """

    entries = data.get("entries", [])

    for day in entries:
        if day["date"] == get_current_date_day():
            return day

    new_day = {"date": date, "tasks": [], "notes": ""}
    entries.append(new_day)
    return new_day


def add_task(task_name: str) -> None:
    """
    Add a new checkbox (i.e. task) under today's '### Tasks' section using a JSON-first approach.
    """
    json_path = get_json_file_path()
    file_path = get_file_path()
    date = get_current_date()
    data = load_json(json_path)
    day = create_new_day(data, date)

    # Extract tag if the task starts with backticks.
    tag_match = re.match(r"`(.*?)`\s*(.*)", task_name)
    if tag_match:
        tag = tag_match.group(1).strip()
        task_name = tag_match.group(2).strip()
    else:
        tag = "UNTAGGED"

    day["tasks"].append(
        {
            "name": task_name,
            "completed": False,
            "started_date": date,  # YYYY-MM-DD
            "tag": tag,
        }
    )
    save_json(json_path, data)
    write_markdown(file_path, data)
    print(f"Added task: {task_name[:32]}")


def prompt_for_task() -> None:
    """
    Prompt the user for a task interactively.
    """
    task = input("Task: ").strip()
    if not task:
        print("Task cannot be empty. Aborting.")
        return

    add_task(task)


def add_note(new_note: str) -> None:
    """
    Add a new note under today's '### Notes' section as a single text block.
    """
    json_path = get_json_file_path()
    file_path = get_file_path()
    data = load_json(json_path)
    today = get_current_date_day()  # e.g., "YYYY-MM-DD"

    day = create_new_day(data, today)

    # Append the new note to the existing notes, ensuring a blank line between notes.
    if day["notes"]:
        day["notes"] += f"\n\n{new_note}"
    else:
        day["notes"] = new_note

    save_json(json_path, data)
    write_markdown(file_path, data)
    print(f"Added note: {new_note[:32]}...")


def prompt_for_note() -> None:
    """
    Prompt the user for a task interactively.
    """
    note = input("Note: ").strip()
    if not note:
        print("Note cannot be empty. Aborting.")
        return

    add_note(note)


def check_off_task(task_number: int) -> None:
    """
    Mark a specific task as completed based on its position in the list
    of unfinished tasks.
    """
    json_path = get_json_file_path()
    file_path = get_file_path()
    data = load_json(json_path)
    entries = data.get("entries", [])

    current_task_count = 0
    task_found = False

    for day in entries:
        for task in day["tasks"]:
            if not task["completed"]:
                current_task_count += 1
                if current_task_count == task_number:
                    task["completed"] = True
                    task["completed_date"] = day["date"]
                    task_found = True
                    break
        if task_found:
            break

    if task_found:
        save_json(json_path, data)
        write_markdown(file_path, data)
        print_unfinished_tasks()

        print(f"\nTask {task_number} has been checked off.")
    else:
        print("Invalid task number.")


def load_unfinished_tasks_from_data(data: Dict[str, List[Dict]]) -> list:
    """
    Extract all unfinished tasks from the given data (list of day dictionaries).
    """
    tasks = []
    entries = data.get("entries", [])
    for day in entries:
        tasks.extend([task for task in day["tasks"] if not task["completed"]])
    return tasks


def get_or_create_today_section(data: Dict[str, List[Dict]], today: str) -> dict:
    """
    Return the section corresponding to today's date in the data.
    If not present, create a new section.
    """
    entries = data.get("entries", [])
    today_section = next((e for e in entries if e["date"] == today), None)
    if not today_section:
        today_section = {"date": today, "tasks": [], "notes": ""}
        entries.append(today_section)
    return today_section


def remove_unfinished_from_previous_days(
    data: Dict[str, List[Dict]], today: str
) -> None:
    """
    For every day in data that is not today, remove tasks that are still unfinished.
    """
    entries = data.get("entries", [])
    for day in entries:
        if day["date"] != today:
            day["tasks"] = [task for task in day["tasks"] if task["completed"]]


def move_unchecked() -> None:
    """
    Move all unfinished tasks from the current and previous month to today's date.
    """

    def safe_load_json(path):
        """
        Load JSON safely, returning a dict with 'entries' key.
        """
        if path and os.path.exists(path):
            return load_json(path)
        print(f"Warning: JSON file not found: {path}")
        return {"entries": []}

    today = get_current_date_day()
    file_path = get_file_path()
    current_json_path = get_json_file_path()
    prev_json_path = get_prev_json_file_path()
    current_data = safe_load_json(current_json_path)
    prev_data = safe_load_json(prev_json_path)
    current_unfinished = load_unfinished_tasks_from_data(current_data)
    prev_unfinished = load_unfinished_tasks_from_data(prev_data)
    unchecked_tasks = current_unfinished + prev_unfinished
    if not unchecked_tasks:
        print("No unfinished tasks to move.")
        return
    today_section = get_or_create_today_section(current_data, today)

    # Prevent duplicates in today's tasks
    existing_task_names = {task["name"] for task in today_section["tasks"]}
    unique_tasks = [
        task for task in unchecked_tasks if task["name"] not in existing_task_names
    ]

    # Add unique tasks and clean up old unfinished tasks
    today_section["tasks"].extend(unique_tasks)
    remove_unfinished_from_previous_days(current_data, today)

    save_json(current_json_path, current_data)
    if prev_data["entries"]:  # Only save if there were previous entries
        save_json(prev_json_path, prev_data)
    write_markdown(file_path, current_data)
    print(f"Moved {len(unique_tasks)} unfinished tasks to today.")
