#!/usr/bin/env python3

################################################################################
# daily.py
#
# Description:
#   This script manages a daily notes markdown file. You can add tasks and notes to a day,
#   mark a note as completed, list unfinished or finished tasks, move unfinished tasks to
#   the current day, and open the file in an editor or a rendered markdown viewer.
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
#   -o, --open               Open the current month's markdown file in a rendered markdown viewer.
#   -t, --task               Add a new task to today's section.
#   -u, --update             Move all unchecked tasks to today's section.
#
# Notes:
#   - Tasks added will include the current date in the format "(MM-DD)".
#   - The notes file is automatically organized by month and year. Each month
#     has its own markdown file located in "~/Notes/Daily/YYYY/YYYY_MM_monthname.md".
#   - Tasks are saved under "### Tasks" and notes under "### Notes" for each day.
#
################################################################################


from parsing import parse_markdown
from notes import interactive_add_note
from cli import parse_arguments
from editor import open_file_in_vim, open_file_in_browser
from tasks import (
    check_off_task,
    list_unfinished_tasks,
    print_completed_tasks,
    print_tasks_by_tag,
    list_task_tags,
    move_unchecked,
    interactive_add_task,
)
from date_paths import (
    get_current_year,
    get_current_month,
    get_current_month_name,
    get_current_year_dir,
    get_file_path,
    get_json_file_path,
)

year = get_current_year()
month = get_current_month()
month_name = get_current_month_name()
file_path = get_file_path()
json_path = get_json_file_path()
year_dir = get_current_year_dir()


if __name__ == "__main__":
    args = parse_arguments()

    COMMANDS = {
        "check": lambda: check_off_task(file_path, args.check),
        "edit": lambda: open_file_in_vim(file_path),
        "list": lambda: list_unfinished_tasks(json_path),
        "list_completed": lambda: print_completed_tasks(json_path),
        "list_tag": lambda: print_tasks_by_tag(json_path, args.list_tag),
        "list_tags": lambda: list_task_tags(file_path),
        "note": lambda: interactive_add_note(file_path),
        "open": lambda: open_file_in_browser(file_path),
        "task": lambda: interactive_add_task(file_path),
        "update": lambda: move_unchecked(year_dir),
    }

    for cmd, func in COMMANDS.items():
        if getattr(args, cmd):
            func()
            break
    else:
        print("Invalid command. Use --help for usage information.")
