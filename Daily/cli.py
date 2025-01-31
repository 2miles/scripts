import argparse


def parse_arguments():
    """Parse command-line arguments for the daily notes manager."""
    parser = argparse.ArgumentParser(description="Manage your daily notes.")

    parser.add_argument(
        "-c",
        "--check",
        type=int,
        help="Check off a task by its number (use -l to list tasks)",
    )
    parser.add_argument(
        "-e", "--edit", action="store_true", help="Open file in vim for editing"
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List all unfinished tasks"
    )
    parser.add_argument(
        "-lc", "--list-completed", action="store_true", help="List all completed tasks"
    )
    parser.add_argument(
        "-lt",
        "--list-tag",
        type=str,
        help="List all tasks with the given tag inside backticks",
    )
    parser.add_argument(
        "-ltags",
        "--list-tags",
        action="store_true",
        help="List all unique tags used in tasks",
    )
    parser.add_argument(
        "-n", "--note", action="store_true", help="Add a new note interactively"
    )
    parser.add_argument(
        "-o",
        "--open",
        action="store_true",
        help="Open file in a rendered markdown viewer",
    )
    parser.add_argument(
        "-t",
        "--task",
        action="store_true",
        help="Add a new task interactively or specify a single task as an argument",
    )
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Move unchecked tasks to the most recent day",
    )

    return parser.parse_args()
