import os
import re
from parsing import parse_markdown, write_markdown
from typing import List, Dict
from json_handler import load_json, save_json

from date_paths import (
    get_current_date,
    get_current_date_day,
)

date = get_current_date()
date_day = get_current_date_day()


def create_new_day(data: List[Dict], date: str) -> Dict:
    """Ensure today's section exists in the data."""

    # Check if this formatted date already exists in the data
    for day in data:
        if day["date"] == date_day:
            return day  # Return the existing entry

    # If not found, create a new entry
    new_day = {"date": date, "tasks": [], "notes": ""}
    data.append(new_day)
    return new_day


def add_checkbox(file_path: str, task_name: str) -> None:
    """Add a new checkbox under today's '### Tasks' section."""
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


def interactive_add_task(file_path: str) -> None:
    """Prompt the user for a task interactively."""
    task = input("Task: ").strip()
    if not task:
        print("Task cannot be empty. Aborting.")
        return

    add_checkbox(file_path, task)


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


def list_unfinished_tasks(json_path: str, silent: bool = False) -> List[tuple]:
    """
    List all unfinished tasks across all days from JSON.
    If `silent=True`, it returns the list without printing.
    """

    data = load_json(json_path)
    unfinished_tasks = []
    task_counter = 1

    if not silent:
        print(
            "\n*******************************************************************************"
        )
        print(
            "|                           All Unfinished Tasks                              |"
        )
        print(
            "*******************************************************************************\n"
        )

    for day in data:
        for task in day["tasks"]:
            if not task["completed"]:
                truncated_name = task["name"][:45]
                if len(task["name"]) > 45:
                    truncated_name += "..."

                unfinished_tasks.append(
                    (task_counter, task["name"])
                )  # ✅ Structured reference

                if not silent:
                    print(
                        f"{task_counter:<3}  {task['tag']:<10}   {truncated_name:<48}   {task['started_date']}"
                    )

                task_counter += 1

    if not unfinished_tasks and not silent:
        print("No unfinished tasks.")

    return unfinished_tasks


def list_completed_tasks(json_path: str) -> None:
    """List all completed tasks across all days from JSON."""

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
            completed_tasks.append(f"## {day['date']}")
            completed_tasks.extend(
                [
                    f"- [x] {task['tag']} {task['name']} {task['started_date']}".strip()
                    for task in day_tasks
                ]
            )
            completed_tasks.append("")

    output = "\n".join(completed_tasks)
    if not output.strip():
        print("No completed tasks found.")
    else:
        print(output)


# Regex pattern for valid filenames (e.g., 2025_1_jan.md, 2025_12_dec.md)
VALID_FILENAME_PATTERN = re.compile(r"^\d{4}_\d{1,2}_[a-z]+\.md$", re.IGNORECASE)


def move_unchecked(year_dir: str) -> None:
    """Move all unchecked tasks from all valid monthly files in a given year directory to the most recent date."""

    if not os.path.isdir(year_dir):
        print(f"Error: '{year_dir}' is not a valid directory.")
        return

    all_tasks = []
    file_data = {}

    # Get markdown files that match the expected format
    md_files = sorted(
        [f for f in os.listdir(year_dir) if VALID_FILENAME_PATTERN.match(f)],
        key=lambda f: f.lower(),  # Sort alphabetically, assuming chronological naming
    )

    if not md_files:
        print(f"No valid markdown files found in {year_dir}.")
        return

    # Process each file and collect unchecked tasks
    for file_name in md_files:
        file_path = os.path.join(year_dir, file_name)
        data = parse_markdown(file_path)
        file_data[file_path] = data  # Store parsed data for later writing

        for day in data:
            unchecked_tasks = [task for task in day["tasks"] if not task["completed"]]

            # ✅ Prevent duplicates before adding to all_tasks
            for task in unchecked_tasks:
                if task not in all_tasks:
                    all_tasks.append(task)

            # ✅ Remove only unchecked tasks from previous days
            day["tasks"] = [task for task in day["tasks"] if task["completed"]]

    if not all_tasks:
        print("No unchecked tasks to move.")
        return

    # Move unchecked tasks to today's date
    most_recent_file = os.path.join(year_dir, md_files[-1])
    most_recent_data = file_data[most_recent_file]

    most_recent_day = create_new_day(most_recent_data, date)  # It will auto-format

    # ✅ Prevent duplicates from being added again
    existing_task_names = {task["name"] for task in most_recent_day["tasks"]}
    unique_tasks = [
        task for task in all_tasks if task["name"] not in existing_task_names
    ]

    most_recent_day["tasks"].extend(unique_tasks)  # ✅ Only add unique tasks

    # Write back only modified files
    for file_path, data in file_data.items():
        write_markdown(file_path, data)

    print(
        f"Moved {len(unique_tasks)} unchecked tasks to {most_recent_day['date']} in {os.path.basename(most_recent_file)}."
    )


def list_tasks_by_tag(file_path: str, tag: str) -> None:
    """List all tasks that contain the given tag inside backticks, case-insensitively."""
    data = parse_markdown(file_path)
    tagged_tasks: List[str] = []
    tag_lower = tag.lower()

    print(f"\nTasks with tag `{tag}`:\n")
    for day in data:
        for task in day["tasks"]:
            if tag_lower in task["name"].lower():
                status = "[x]" if task["completed"] else "[ ]"
                tagged_tasks.append(f"- {status} {task['name']} ({day['date']})")

    if tagged_tasks:
        print("\n".join(tagged_tasks))
    else:
        print(f"No tasks found with tag `{tag}`.")


def list_task_tags(file_path: str) -> None:
    """List all unique tags used in tasks."""
    data = parse_markdown(file_path)
    tags = set()

    for day in data:
        for task in day["tasks"]:
            match = re.match(r"`([^`]*)`", task["name"])
            if match:
                tags.add(match.group(1))

    if tags:
        print("\nTags in use:")
        print("\n".join(sorted(tags)))
    else:
        print("No tags found.")
