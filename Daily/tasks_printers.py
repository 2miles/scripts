from tasks_getters import (
    get_completed_tasks,
    get_tags,
    get_tasks_by_tag,
    get_unfinished_tasks,
)


def print_unfinished_tasks() -> None:
    """
    Print all unfinished tasks.
    """
    unfinished_tasks = get_unfinished_tasks()

    print("\n                           All Unfinished Tasks\n")
    if not unfinished_tasks:
        print("No unfinished tasks.")
        return
    for task_count, tag, short_name, started_date in unfinished_tasks:
        print(f"{task_count:<3}  {tag:<10}  {short_name:<48}  {started_date}")


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
