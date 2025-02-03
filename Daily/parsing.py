from datetime import datetime
import os
import re
from typing import List, Dict, Any, Optional


def parse_markdown(file_path: str) -> List[Dict[str, Any]]:
    """Parse the markdown file, extracting tasks with tags and started dates."""
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
                        task_text = line[6:].strip()  # Remove checkbox prefix
                        # Remove trailing "--" if present
                        # task_text = re.sub(r"\s*--\s*$", "", task_text)
                        task_text = re.sub(
                            r"\s*--(?=\s*\(\d{2}-\d{2}\)$)", "", task_text
                        ).strip()

                        # Extract started_date (if present)
                        started_date_match = re.search(r"\((\d{2}-\d{2})\)$", task_text)
                        if started_date_match:
                            month_day = started_date_match.group(1)
                            started_date = f"{current_day['date'][:4]}-{month_day}"  # Convert to YYYY-MM-DD
                            task_text = re.sub(
                                r"\(\d{2}-\d{2}\)$", "", task_text
                            ).strip()  # Remove (MM-DD)
                        else:
                            started_date = current_day["date"]  # Default if missing

                        # Extract tag (if present)
                        tag_match = re.match(r"`(.*?)`\s*(.*)", task_text)
                        if tag_match:
                            tag = (
                                tag_match.group(1).strip()
                                if tag_match.group(1).strip()
                                else "UNTAGGED"
                            )
                            task_name = tag_match.group(2).strip()
                        else:
                            tag = "UNTAGGED"
                            task_name = task_text.strip()

                        tasks_buffer.append(
                            {
                                "name": task_name,
                                "completed": completed,
                                "started_date": started_date,
                                "tag": tag,
                            }
                        )
                elif in_notes_section:
                    notes_buffer.append(line)

        if current_day:
            current_day["notes"] = "\n".join(notes_buffer).strip()
            current_day["tasks"] = tasks_buffer
            data.append(current_day)

    return data


def write_markdown(file_path: str, data: List[Dict]) -> None:
    """Write structured task and note data back to a markdown file."""
    with open(file_path, "w") as file:
        for day in data:
            file.write(f"\n## {day['date']}\n\n")  # No reformatting needed

            if day["tasks"]:
                file.write("### Tasks\n\n")
                for task in day["tasks"]:
                    status = "[x]" if task["completed"] else "[ ]"

                    # Format task name with tag
                    task_name = (
                        f"`{task['tag']}` {task['name']}"
                        if task["tag"]
                        else task["name"]
                    )

                    # Convert started_date from YYYY-MM-DD to (MM-DD)
                    if task["started_date"]:
                        formatted_date = f"({task['started_date'][5:]})"
                        task_name += f" {formatted_date}"

                    file.write(f"- {status} {task_name}\n")

                file.write("\n")

            if day["notes"]:
                file.write("### Notes\n\n")
                file.write(f"{day['notes']}\n\n")
