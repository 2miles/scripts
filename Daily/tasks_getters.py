from collections import defaultdict
from typing import Dict, List, Tuple

from date_paths import get_json_file_path
from json_handler import load_json


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
