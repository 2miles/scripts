import re
from parsing import parse_markdown, write_markdown
from datetime import datetime
from typing import List, Dict

# Constants for date formatting
CURRENT_DATE: str = datetime.now().strftime("%Y-%m-%d")
CURRENT_DAY: str = datetime.now().strftime("%a")


def create_new_day(data: List[Dict], date: str) -> Dict:
    """Ensure today's section exists in the data."""
    for day in data:
        if day["date"] == date:
            return day
    new_day = {"date": date, "tasks": [], "notes": ""}
    data.append(new_day)
    return new_day


def add_checkbox(file_path: str, task_name: str) -> None:
    """Add a new checkbox under today's '### Tasks' section."""
    data = parse_markdown(file_path)
    today = f"{CURRENT_DATE} {CURRENT_DAY}"
    day = create_new_day(data, today)

    # Extract tag if task starts with backticks (e.g.,)
    tag_match = re.match(r"`(.*?)`\s*(.*)", task_name)
    if tag_match:
        tag = tag_match.group(1).strip()
        task_name = tag_match.group(2).strip()
    else:
        tag = "UNTAGGED"

    # Format task with start date
    task_with_date = f"{task_name} -- ({CURRENT_DATE[5:]})"

    # Append task with all required fields
    day["tasks"].append(
        {
            "name": task_name,
            "completed": False,
            "started_date": CURRENT_DATE,  # YYYY-MM-DD
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


def check_off_task(file_path: str, task_number: int) -> None:
    """Mark a specific task as completed."""
    data = parse_markdown(file_path)
    task_counter = 1

    for day in data:
        for task in day["tasks"]:
            if not task["completed"]:
                if task_counter == task_number:
                    task["completed"] = True
                    write_markdown(file_path, data)
                    print(f"Task {task_number} has been checked off: {task['name']}")
                    return
                task_counter += 1

    print(f"Task {task_number} not found.")


def list_unfinished_tasks(file_path: str) -> None:
    """List all unfinished tasks across all days."""
    data = parse_markdown(file_path)
    unfinished_tasks: List[str] = []
    task_counter: int = 1
    print()
    print(
        "****************************************************************************"
    )
    print(
        "|                          All Unfinished Tasks                            |"
    )
    print(
        "****************************************************************************"
    )
    print()
    for day in data:
        for task in day["tasks"]:
            if not task["completed"]:
                truncated_name = task["name"][:45]
                if len(truncated_name) > 44:
                    truncated_name = truncated_name + "..."

                unfinished_tasks.append(
                    f"{task_counter}.  {task['tag']:<8}   {truncated_name:<48}   {task['started_date']}"
                )
                task_counter += 1

    if not unfinished_tasks:
        print("No unfinished tasks.")
        return

    print("\n".join(unfinished_tasks))


def list_completed_tasks(file_path: str) -> None:
    """List all completed tasks across all days, including tags and started dates."""
    data = parse_markdown(file_path)
    completed_tasks: List[str] = []

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


def move_unchecked(file_path: str) -> None:
    """Move all unchecked tasks to the most recent date."""
    data = parse_markdown(file_path)
    today = f"{CURRENT_DATE} {CURRENT_DAY}"
    most_recent_day = create_new_day(data, today)

    moved_tasks: List[Dict] = []
    for day in data:
        if day["date"] != today:
            unchecked = [task for task in day["tasks"] if not task["completed"]]
            moved_tasks.extend(unchecked)
            day["tasks"] = [task for task in day["tasks"] if task["completed"]]

    if not moved_tasks:
        print("No unchecked tasks to move.")
        return

    most_recent_day["tasks"].extend(moved_tasks)
    write_markdown(file_path, data)
    print(f"Moved {len(moved_tasks)} unchecked tasks to {today}.")


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
