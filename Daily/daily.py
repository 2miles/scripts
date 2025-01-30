#!/usr/bin/env python3

################################################################################
# daily.py
#
# Description:
#   This script manages a daily notes file in markdown format. It allows users
#   to add tasks, notes, toggle task completion, list unfinished tasks, list
#   completed tasks, move unchecked tasks to the most recent day, and open the
#   file in an editor or a rendered markdown viewer.
#
# Usage:
#   python daily.py [OPTIONS]
#
# Options:
#   -c, --check NUMBER       Check off a task by its enumerated number from the list output by -l.
#   -e, --edit               Open the current month's markdown file in vim for editing.
#   -l, --list               List all unfinished tasks across all days.
#   -lc, --list-completed    List all completed tasks across all days.
#   -lt, --list-tag TAG      List all tasks with the given tag.
#   -n, --note               Add a new note to today's section.
#                            - If no argument is provided, prompts for input interactively.
#   -o, --open               Open the current month's markdown file in a rendered markdown viewer.
#   -t, --task [TASK]        Add a new task to today's section.
#                            - If no argument is provided, prompts for input interactively.
#   -tl, --task-list [TASKS] Add multiple tasks as a list of strings.
#   -u, --update             Move all unchecked tasks to today's section.
#
# Notes:
#   - Tasks added will include the current date in the format "(MM-DD)".
#   - The notes file is automatically organized by month and year. Each month
#     has its own markdown file located in "~/Notes/Daily/YYYY/YYYY_MM_monthname.md".
#   - Tasks are saved under "### Tasks" and notes under "### Notes" for each day.
#
################################################################################

import os
from datetime import datetime
from editor import open_file_in_vim, open_file_in_browser
from parsing import parse_markdown
from tasks import (
    add_checkbox,
    add_multiple_checkboxes,
    check_off_task,
    list_unfinished_tasks,
    list_completed_tasks,
    move_unchecked,
    list_tasks_by_tag,
    list_task_tags,
)
from notes import interactive_add_note
from cli import parse_arguments

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

if __name__ == "__main__":
    args = parse_arguments()
    data = parse_markdown(FILE_PATH)

    COMMANDS = {
        "check": lambda: check_off_task(FILE_PATH, args.check),
        "edit": lambda: open_file_in_vim(FILE_PATH),
        "list": lambda: list_unfinished_tasks(FILE_PATH),
        "list_completed": lambda: list_completed_tasks(FILE_PATH),
        "list_tag": lambda: list_tasks_by_tag(FILE_PATH, args.list_tag),
        "list_tags": lambda: list_task_tags(FILE_PATH),
        "note": lambda: interactive_add_note(FILE_PATH),
        "open": lambda: open_file_in_browser(FILE_PATH),
        "task": lambda: add_checkbox(FILE_PATH, args.task),
        "task_list": lambda: add_multiple_checkboxes(FILE_PATH, args.task_list),
        "update": lambda: move_unchecked(FILE_PATH),
    }

    for cmd, func in COMMANDS.items():
        if getattr(args, cmd, None):
            func()
            break
    else:
        print("Invalid command. Use --help for usage information.")
