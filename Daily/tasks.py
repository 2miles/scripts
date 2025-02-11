from collections import defaultdict
import os
import re
from parsing import write_markdown
from typing import List, Dict, Tuple
from json_handler import load_json, save_json

from date_paths import (
    get_current_date,
    get_current_date_day,
    get_file_path,
    get_json_file_path,
    get_prev_json_file_path,
)


def create_new_day(data: List[Dict], date: str) -> Dict:
    """
    Ensure today's section exists in the data.
    """
    for day in data:
        if day["date"] == get_current_date_day():
            return day
    new_day = {"date": date, "tasks": [], "notes": ""}
    data.append(new_day)
    return new_day


def add_checkbox(task_name: str) -> None:
    """Add a new checkbox (i.e. task) under today's '### Tasks' section using a JSON-first approach."""
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

    add_checkbox(task)


def check_off_task(task_number: int) -> None:
    """
    Mark a specific task as completed based on its position in the list
    of unfinished tasks.
    """
    json_path = get_json_file_path()
    file_path = get_file_path()
    data = load_json(json_path)

    current_task_count = 0
    task_found = False

    for day in data:
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
        print(f"Task {task_number} has been checked off.")
    else:
        print("Invalid task number.")


def get_unfinished_tasks() -> List[Tuple[int, str, str, str]]:
    """Retrieve all unfinished tasks from JSON."""
    data = load_json(get_json_file_path())
    unfinished_tasks = []
    task_count = 1

    for day in data:
        for task in day["tasks"]:
            if not task["completed"]:
                short_name = task["name"][:45]
                if len(task["name"]) > 45:
                    short_name += "..."
                unfinished_tasks.append(
                    (task_count, task["tag"], short_name, task["started_date"])
                )
                task_count += 1

    return unfinished_tasks


def print_unfinished_tasks() -> None:
    """Print all unfinished tasks."""
    unfinished_tasks = get_unfinished_tasks()

    print()
    print("                           All Unfinished Tasks")
    print()
    if not unfinished_tasks:
        print("No unfinished tasks.")
        return

    for task_count, tag, short_name, started_date in unfinished_tasks:
        print(f"{task_count:<3}  {tag:<10}  {short_name:<48}  {started_date}")


def get_completed_tasks(json_path: str) -> list:
    """
    Retrieve all completed tasks from the current months JSON file.
    """
    data = load_json(json_path)
    completed_tasks = []

    for day in data:
        day_tasks = [
            {
                "name": task["name"],
                "tag": f"[{task['tag']}]" if task["tag"] else "[UNTAGGED]",
                "started_date": (
                    f"(Started: {task['started_date']})" if task["started_date"] else ""
                ),
            }
            for task in day["tasks"]
            if task["completed"]
        ]
        if day_tasks:
            completed_tasks.append({"date": day["date"], "tasks": day_tasks})

    return completed_tasks


def print_completed_tasks(json_path: str) -> None:
    """
    Print all completed tasks in the current month's JSON file.
    """
    completed_tasks = get_completed_tasks(json_path)
    if not completed_tasks:
        print("No completed tasks found.")
        return

    output = []
    for day in completed_tasks:
        output.append(f"## {day['date']}")
        output.extend(
            [
                f"- [x] {task['tag']} {task['name']} {task['started_date']}".strip()
                for task in day["tasks"]
            ]
        )
        output.append("")
    print("\n".join(output))


def load_unfinished_tasks_from_data(data: list) -> list:
    """
    Extract all unfinished tasks from the given data (list of day dictionaries).
    """
    tasks = []
    for day in data:
        tasks.extend([task for task in day["tasks"] if not task["completed"]])
    return tasks


def get_or_create_today_section(data: list, today: str) -> dict:
    """
    Return the section corresponding to today's date in the data.
    If not present, create a new section.
    """
    today_section = next((d for d in data if d["date"] == today), None)
    if not today_section:
        today_section = {"date": today, "tasks": [], "notes": ""}
        data.append(today_section)
    return today_section


def remove_unfinished_from_previous_days(data: list, today: str) -> None:
    """
    For every day in data that is not today, remove tasks that are still unfinished.
    """
    for day in data:
        if day["date"] != today:
            day["tasks"] = [task for task in day["tasks"] if task["completed"]]


def move_unchecked() -> None:
    """
    Move all unfinished tasks from the current and previous month to today's date.
    """
    today = get_current_date_day()
    file_path = get_file_path()
    current_json_path = get_json_file_path()
    prev_json_path = get_prev_json_file_path()

    # Load current month data and its unfinished tasks.
    if os.path.exists(current_json_path):
        current_data = load_json(current_json_path)
        current_unfinished = load_unfinished_tasks_from_data(current_data)
    else:
        print(f"Warning: Current month JSON file not found: {current_json_path}")
        current_data = []
        current_unfinished = []

    # Load previous month data and its unfinished tasks, if available.
    prev_unfinished = []
    prev_data = []
    if prev_json_path and os.path.exists(prev_json_path):
        prev_data = load_json(prev_json_path)
        prev_unfinished = load_unfinished_tasks_from_data(prev_data)

    # Combine unfinished tasks from both months.
    unchecked_tasks = current_unfinished + prev_unfinished
    if not unchecked_tasks:
        print("No unfinished tasks to move.")
        return

    today_section = get_or_create_today_section(current_data, today)

    # Prevent duplicate tasks in today's section.
    existing_task_names = {task["name"] for task in today_section["tasks"]}
    unique_tasks = [
        task for task in unchecked_tasks if task["name"] not in existing_task_names
    ]

    today_section["tasks"].extend(unique_tasks)
    remove_unfinished_from_previous_days(current_data, today)
    save_json(current_json_path, current_data)
    if prev_data:
        save_json(prev_json_path, prev_data)
    write_markdown(file_path, current_data)
    print(f"Moved {len(unique_tasks)} unfinished tasks to today.")


def get_tasks_by_tag(json_path: str, tag: str) -> list:
    """
    Retrieve all tasks that contain the given tag (case-insensitive) from JSON.
    """
    data = load_json(json_path)

    tag_lower = tag.lower()
    tasks: List[str] = []

    for day in data:
        day_tasks = [
            {"name": task["name"], "completed": task["completed"], "date": day["date"]}
            for task in day["tasks"]
            if tag_lower in task["tag"].lower()
        ]
        if day_tasks:
            tasks.append({"date": day["date"], "tasks": day_tasks})

    return tasks


def print_tasks_by_tag(json_path: str, tag: str) -> None:
    """
    Print all tasks that contain the given tag in a structured format.
    """
    tagged_tasks = get_tasks_by_tag(json_path, tag)
    if not tagged_tasks:
        print(f"No tasks found with tag `{tag}`.")
        return
    output = [f"\nTasks with tag `{tag}`:\n"]
    for day in tagged_tasks:
        for task in day["tasks"]:
            status = "[x]" if task["completed"] else "[ ]"
            output.append(f"- {status} {task['name']} ({day['date']})")
    print("\n".join(output))


def get_tags(json_path: str) -> Dict[str, int]:
    """
    Retrieve all unique tags used and their counts.
    """
    data = load_json(json_path)
    tag_counts: Dict[str, int] = defaultdict(int)
    for day in data:
        for task in day.get("tasks", []):
            if "tag" in task and task["tag"]:
                tag_counts[task["tag"]] += 1

    return dict(sorted(tag_counts.items()))


def print_tags(json_path: str) -> None:
    """
    Print all unique tags and their counts.
    """
    tags = get_tags(json_path)
    if tags:
        print("\nTags in use:\n")
        pad_char = "."
        for tag, count in tags.items():
            print(f"{tag:{pad_char}<16} {count}")
    else:
        print("No tags found.")
