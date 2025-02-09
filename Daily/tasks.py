from collections import defaultdict
import os
import re
from parsing import parse_markdown, write_markdown
from typing import List, Dict, Set, Tuple
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
    # Check if this formatted date already exists in the json
    for day in data:
        if day["date"] == get_current_date_day():
            return day  # Return the existing entry

    # If not found, create a new entry
    new_day = {"date": date, "tasks": [], "notes": ""}
    data.append(new_day)
    return new_day


## NEEDS TO BE CONVERTED
def add_checkbox(file_path: str, task_name: str) -> None:
    """Add a new checkbox under today's '### Tasks' section."""
    date = get_current_date()
    data = parse_markdown(file_path)
    day = create_new_day(data, date)

    # Extract tag if task starts with backticks (e.g.,)
    tag_match = re.match(r"`(.*?)`\s*(.*)", task_name)
    if tag_match:
        tag = tag_match.group(1).strip()
        task_name = tag_match.group(2).strip()
    else:
        tag = "UNTAGGED"

    # Format task with start date
    task_with_date = f"{task_name} -- ({date[5:]})"

    # Append task with all required fields
    day["tasks"].append(
        {
            "name": task_name,
            "completed": False,
            "started_date": date,  # YYYY-MM-DD
            "tag": tag,  # Always there
        }
    )

    write_markdown(file_path, data)
    print(f"Added task: {task_with_date[:32]}...")


## NEEDS TO BE CONVERTED
def interactive_add_task(file_path: str) -> None:
    """Prompt the user for a task interactively."""
    task = input("Task: ").strip()
    if not task:
        print("Task cannot be empty. Aborting.")
        return

    add_checkbox(file_path, task)


## NEEDS TO BE CONVERTED
def check_off_task(json_path: str, task_number: int) -> None:
    """Mark a specific task as completed using the task name instead of a dynamic number."""

    data = load_json(json_path)
    unfinished_tasks = list_unfinished_tasks(json_path, True)

    if task_number < 1 or task_number > len(unfinished_tasks):
        print("Invalid task number.")
        return
    selected_task_name = unfinished_tasks[task_number - 1][1]
    # Search for this task in JSON and mark it as complete
    for day in data:
        for task in day["tasks"]:
            if task["name"] == selected_task_name:
                task["completed"] = True
                save_json(json_path, data)  # ✅ Save the updated JSON
                print(f"Task {task_number} has been checked off: {task['name']}")
                return

    print(f"Task {task_number} not found.")


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


def print_unfinished_tasks():
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
    Retrieve all completed tasks from JSON.
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
    Print all completed tasks in a structured format.
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


def move_unchecked() -> None:
    """Move all unfinished tasks from the current and previous month to today's date."""
    today = get_current_date_day()
    file_path = get_file_path()
    current_json_path = get_json_file_path()
    prev_json_path = get_prev_json_file_path()

    unchecked_tasks = []

    # Load current and previous months JSON and collect unfinished tasks
    if os.path.exists(current_json_path):
        current_data = load_json(current_json_path)
        for day in current_data:
            unchecked_tasks.extend(
                [task for task in day["tasks"] if not task["completed"]]
            )
    else:
        print(f"Warning: Current month JSON file not found: {current_json_path}")
        current_data = []
    if prev_json_path and os.path.exists(prev_json_path):
        prev_data = load_json(prev_json_path)
        for day in prev_data:
            unchecked_tasks.extend(
                [task for task in day["tasks"] if not task["completed"]]
            )
    if not unchecked_tasks:
        print("No unfinished tasks to move.")
        return

    # ✅ Find or create today's section in JSON
    today_section = next((d for d in current_data if d["date"] == today), None)
    if not today_section:
        today_section = {"date": today, "tasks": [], "notes": ""}
        current_data.append(today_section)

    # ✅ Prevent duplicate tasks
    existing_task_names = {task["name"] for task in today_section["tasks"]}
    unique_tasks = [
        task for task in unchecked_tasks if task["name"] not in existing_task_names
    ]

    today_section["tasks"].extend(unique_tasks)

    # ✅ Remove unfinished tasks from previous days
    for day in current_data:
        if day["date"] != today:
            day["tasks"] = [task for task in day["tasks"] if task["completed"]]

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

    return dict(sorted(tag_counts.items()))  # Sort alphabetically by tag


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
