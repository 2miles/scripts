#!/usr/bin/env python3

################################################################################
# daily_notes.py
#
# Description:
#   This script manages a daily notes file in markdown format. It allows users
#   to add tasks, notes, move unchecked tasks to the most recent day, view
#   unfinished tasks, check off specific tasks, and open the file in an editor
#   or a rendered markdown viewer.
#
# Usage:
#   ./daily_notes.py [OPTIONS]
#
# Options:
#   -t, --task TASK        Add a new task to today's section with the current date.
#   -n, --note NOTE        Add a new note to today's section.
#   -u, --update           Move all unchecked tasks to today's section.
#   -o, --open             Open the current month's markdown file in the default
#                          markdown viewer (e.g., using grip).
#   -e, --edit             Open the current month's markdown file in vim for editing.
#   -l, --list             List all unfinished tasks across all days.
#   -c, --check NUMBER     Check off a task by its enumerated number from the list
#                          output by the -l option.
#
# Example usage:
#   ./daily_notes.py -t "Complete project report"
#     - Adds a new task to today's "### Tasks" section:
#       "- [ ] Complete project report -- (01-26)"
#
#   ./daily_notes.py -n "Meeting at 10 AM"
#     - Adds a new note to today's "### Notes" section:
#       "Meeting at 10 AM"
#
#   ./daily_notes.py -u
#     - Moves all unchecked tasks from previous days to today's section.
#
#   ./daily_notes.py -l
#     - Lists all unfinished tasks, enumerated, with their dates.
#
#   ./daily_notes.py -c 3
#     - Marks task #3 (from the -l output) as completed.
#
#   ./daily_notes.py -o
#     - Opens the current month's markdown file in a rendered markdown viewer.
#
#   ./daily_notes.py -e
#     - Opens the current month's markdown file in vim for editing.
#
# Notes:
#   - Tasks added will include the current date in the format "(MM-DD)".
#   - The notes file is automatically organized by month and year. Each month
#     has its own markdown file located in "~/Notes/Daily/YYYY/YYYY_MM_monthname.md".
#   - Tasks are saved under "### Tasks" and notes under "### Notes" for each day.
#
################################################################################

import os
import subprocess
from datetime import datetime
import argparse
from typing import List, Dict, Any, Optional

# Constants for directories and file paths
BASE_DIR: str = os.path.expanduser("~/Notes/Daily")
CURRENT_DATE: str = datetime.now().strftime("%Y-%m-%d")
CURRENT_DAY: str = datetime.now().strftime("%a")
CURRENT_YEAR: str = datetime.now().strftime("%Y")
CURRENT_MONTH: str = datetime.now().strftime("%m").lstrip("0")
CURRENT_MONTH_NAME: str = datetime.now().strftime("%b").lower()

# Path to the current month's file
FILE_PATH: str = os.path.join(
    BASE_DIR, CURRENT_YEAR, f"{CURRENT_YEAR}_{CURRENT_MONTH}_{CURRENT_MONTH_NAME}.md"
)

# Ensure the directories and file exist
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as file:
        pass


def parse_markdown(file_path: str) -> List[Dict[str, Any]]:
    """Parse the markdown file into a JSON-like structure."""
    data: List[Dict] = []
    current_day: Optional[Dict] = None

    if not os.path.exists(file_path):
        return data

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("## "):  # Date header
                if current_day:
                    data.append(current_day)
                current_day = {"date": line[3:], "tasks": [], "notes": []}
            elif current_day is not None:  # Ensure current_day is initialized
                if line.startswith("- [ ]") or line.startswith("- [x]"):  # Task
                    completed: bool = line.startswith("- [x]")
                    task_name: str = line[6:].strip()
                    current_day["tasks"].append(
                        {"name": task_name, "completed": completed}
                    )
                elif line and not line.startswith("###"):  # Note
                    current_day["notes"].append(line)
        if current_day:  # Append the last day
            data.append(current_day)

    return data


def write_markdown(file_path: str, data: List[Dict]) -> None:
    """Write the JSON-like structure back to the markdown file."""
    with open(file_path, "w") as file:
        for day in data:
            file.write(f"## {day['date']}\n\n### Tasks\n\n")
            for task in day["tasks"]:
                status = "[x]" if task["completed"] else "[ ]"
                file.write(f"- {status} {task['name']}\n")
            file.write("\n### Notes\n\n")
            for note in day["notes"]:
                file.write(f"{note}\n\n")
            file.write("\n")


def create_new_day(data: List[Dict], date: str) -> Dict:
    """Ensure today's section exists in the data."""
    for day in data:
        if day["date"] == date:
            return day
    new_day = {"date": date, "tasks": [], "notes": []}
    data.append(new_day)
    return new_day


def add_checkbox(task_name: str) -> None:
    """Add a new checkbox under today's '### Tasks' section."""
    data = parse_markdown(FILE_PATH)
    today = f"{CURRENT_DATE} {CURRENT_DAY}"
    day = create_new_day(data, today)

    task_with_date = f"{task_name} -- ({CURRENT_DATE[5:]})"

    day["tasks"].append({"name": task_with_date, "completed": False})
    write_markdown(FILE_PATH, data)
    print(f"Added task: {task_with_date}")


def add_note(note: str) -> None:
    """Add a new note under today's '### Notes' section."""
    data = parse_markdown(FILE_PATH)
    today = f"{CURRENT_DATE} {CURRENT_DAY}"
    day = create_new_day(data, today)
    day["notes"].append(note)
    write_markdown(FILE_PATH, data)
    print(f"Added note: {note}")


def move_unchecked() -> None:
    """Move all unchecked tasks to the most recent date."""
    data = parse_markdown(FILE_PATH)
    today = f"{CURRENT_DATE} {CURRENT_DAY}"
    most_recent_day = create_new_day(data, today)

    # Gather and move unchecked tasks
    moved_tasks: List[Dict] = []
    for day in data:
        if day["date"] != today:  # Don't move tasks from today's section
            unchecked = [task for task in day["tasks"] if not task["completed"]]
            moved_tasks.extend(unchecked)
            day["tasks"] = [task for task in day["tasks"] if task["completed"]]

    if not moved_tasks:
        print("No unchecked tasks to move.")
        return

    most_recent_day["tasks"].extend(moved_tasks)
    write_markdown(FILE_PATH, data)
    print(f"Moved {len(moved_tasks)} unchecked tasks to {today}.")


def list_unfinished_tasks() -> None:
    """List all unfinished tasks across all days with days difference."""
    data = parse_markdown(FILE_PATH)
    unfinished_tasks: List[str] = []
    task_counter: int = 1

    print("")
    print("**************************************************************************")
    print("*                         All Unfinished Tasks                           *")
    print("**************************************************************************")
    print("")
    for day in data:
        for task in day["tasks"]:
            if not task["completed"]:
                unfinished_tasks.append(f"{task_counter}. {task['name']}")
                task_counter += 1

    if not unfinished_tasks:
        print("No unfinished tasks.")
        return

    print("\n".join(unfinished_tasks))


def check_off_task(task_number: int) -> None:
    """Mark a specific task as completed."""
    data = parse_markdown(FILE_PATH)
    task_counter = 1

    for day in data:
        for task in day["tasks"]:
            if not task["completed"]:
                if task_counter == task_number:
                    task["completed"] = True
                    write_markdown(FILE_PATH, data)
                    print(f"Task {task_number} has been checked off: {task['name']}")
                    return
                task_counter += 1

    print(f"Task {task_number} not found.")


def open_file_in_vim() -> None:
    """Open the file in the default editor at the last unchecked task or the bottom."""
    line_number = None

    # Search for the last line that starts with '- [ ]'
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines, start=1):
                if line.strip().startswith("- [ ]"):
                    line_number = i

    # Open vim at the specified line and move the cursor to the 4th character
    if line_number:
        os.system(
            f"{os.getenv('EDITOR', 'vim')} +{line_number} +'normal 03l' {FILE_PATH}"
        )
    else:
        os.system(f"{os.getenv('EDITOR', 'vim')} + {FILE_PATH}")


def open_file_in_browser() -> None:
    """Render Markdown file to HTML and open it in the browser."""
    html_output = os.path.join(BASE_DIR, "output.html")
    custom_css_url = "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown-dark.min.css"
    subprocess.run(
        [
            "pandoc",
            FILE_PATH,
            "-f",
            "markdown",
            "-t",
            "html",
            "-s",
            "-o",
            html_output,
            "--css",
            custom_css_url,
            "--highlight-style",
            "tango",
        ]
    )
    os.system(f"open {html_output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage your daily notes.")
    parser.add_argument("-t", "--task", help="Add a new task")
    parser.add_argument("-n", "--note", help="Add a new note")
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Move unchecked tasks to the most recent day",
    )
    parser.add_argument(
        "-o",
        "--open",
        action="store_true",
        help="Open file in a rendered markdown viewer",
    )
    parser.add_argument(
        "-e", "--edit", action="store_true", help="Open file in vim for editing"
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all unfinished tasks",
    )
    parser.add_argument(
        "-c",
        "--check",
        type=int,
        help="Check off a task by its number (use -l to list tasks)",
    )
    args = parser.parse_args()

    if args.task:
        add_checkbox(args.task)
    elif args.note:
        add_note(args.note)
    elif args.update:
        move_unchecked()
    elif args.open:
        open_file_in_browser()
    elif args.edit:
        open_file_in_vim()
    elif args.list:
        list_unfinished_tasks()
    elif args.check is not None:
        check_off_task(args.check)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
