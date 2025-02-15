#!/usr/bin/env python3

################################################################################
# daily.py
#
# Description:
#   This script manages a daily notes and tasks system using Markdown and JSON.
#   You can add tasks and notes to a day's entry, check off tasks, list unfinished
#   or completed tasks, move unfinished tasks to today, open files in an editor,
#   sync Markdown files to JSON, and render the file in a browser.
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
#   -ltags, --list-tags      List all unique tags used in tasks.
#   -n, --note               Add a new note to today's section.
#   -o, --open               Open the current month's markdown file in a rendered markdown viewer.
#   -t, --task               Add a new task to today's section.
#   -u, --update             Move all unchecked tasks from the current and previous month to today.
#   -s, --sync [YEAR]        Sync all Markdown files for the given year into JSON.
#                            If no year is provided, it defaults to the current year.
#
# Notes:
#   - Tasks are stored in JSON files under "~/Notes/Daily/YYYY/YYYY_MM_monthname.json".
#   - Each month's data is stored separately, with tasks and notes organized by date.
#   - Tasks are listed under "### Tasks" and notes under "### Notes" in Markdown format.
#   - Tasks include metadata: name, completion status, tag, and start date.
#   - The system follows a JSON-first approach, meaning all modifications sync to JSON
#     first, with Markdown generated as needed.
#   - Syncing updates JSON from Markdown files, ensuring consistency.
#
################################################################################

from datetime import datetime

from cli import parse_arguments
from date_paths import get_file_path, get_json_file_path
from editor import open_file_in_vim, open_file_in_browser
from sync import sync_year
from tasks_core import check_off_task, move_unchecked, prompt_for_note, prompt_for_task
from tasks_printers import (
    print_completed_tasks,
    print_tags,
    print_tasks_by_tag,
    print_unfinished_tasks,
)


if __name__ == "__main__":
    args = parse_arguments()

    file_path = get_file_path()
    json_path = get_json_file_path()

    COMMANDS = {
        "check": lambda: check_off_task(args.check),
        "edit": lambda: open_file_in_vim(file_path),
        "list": lambda: print_unfinished_tasks(),
        "list_completed": lambda: print_completed_tasks(json_path),
        "list_tag": lambda: print_tasks_by_tag(json_path, args.list_tag),
        "list_tags": lambda: print_tags(json_path),
        "note": lambda: prompt_for_note(),
        "open": lambda: open_file_in_browser(file_path),
        "task": lambda: prompt_for_task(),
        "update": lambda: move_unchecked(),
        "sync": lambda: sync_year(args.sync),
    }

    args = parse_arguments()

    # Ensure sync only runs if explicitly requested
    if args.sync is not None and args.sync != datetime.now().year:
        sync_year(args.sync)
    else:
        # Run the first argument that is set
        for cmd, value in vars(args).items():
            if value and cmd in COMMANDS:
                COMMANDS[cmd]()  # Call the associated function
                break
        else:
            print("Invalid command. Use --help for usage information.")
