import os
from typing import List, Dict, Any, Optional


def parse_markdown(file_path: str) -> List[Dict[str, Any]]:
    """Parse the markdown file, treating notes as a single text block and preserving tasks."""
    data: List[Dict[str, Any]] = []
    current_day: Optional[Dict[str, Any]] = None
    in_notes_section = False
    in_tasks_section = False
    notes_buffer = []
    tasks_buffer = []

    if not os.path.exists(file_path):
        return data

    with open(file_path, "r") as file:
        for line in file:
            line = line.rstrip()

            if line.startswith("## "):  # Date header
                if current_day:
                    current_day["notes"] = "\n".join(notes_buffer).strip()
                    current_day["tasks"] = tasks_buffer
                    data.append(current_day)

                current_day = {"date": line[3:], "tasks": [], "notes": ""}
                in_notes_section = False
                in_tasks_section = False
                notes_buffer = []
                tasks_buffer = []

            elif current_day is not None:
                if line.startswith("### Tasks"):
                    in_notes_section = False
                    in_tasks_section = True
                elif line.startswith("### Notes"):
                    in_tasks_section = False
                    in_notes_section = True
                elif in_tasks_section:
                    if line.startswith("- [ ]") or line.startswith("- [x]"):
                        completed = line.startswith("- [x]")
                        task_name = line[6:].strip()
                        tasks_buffer.append({"name": task_name, "completed": completed})
                elif in_notes_section:
                    notes_buffer.append(line)

        if current_day:
            current_day["notes"] = "\n".join(notes_buffer).strip()
            current_day["tasks"] = tasks_buffer
            data.append(current_day)

    return data


def write_markdown(file_path: str, data: List[Dict]) -> None:
    """Write the JSON-like structure back to the markdown file while preserving spacing correctly."""
    with open(file_path, "w") as file:
        for day in data:
            file.write(f"\n## {day['date']}\n\n")

            if day["tasks"]:
                file.write("### Tasks\n\n")
                for task in day["tasks"]:
                    status = "[x]" if task["completed"] else "[ ]"
                    file.write(f"- {status} {task['name']}\n")
                file.write("\n")

            if day["notes"]:
                file.write("### Notes\n\n")
                file.write(f"{day['notes']}\n\n")
