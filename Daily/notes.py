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


def add_note(file_path: str, new_note: str) -> None:
    """Add a new note under today's '### Notes' section as a single text block."""
    data = parse_markdown(file_path)
    today = f"{CURRENT_DATE} {CURRENT_DAY}"
    day = create_new_day(data, today)

    # Ensure a blank line before the new note if there are existing notes
    if day["notes"]:
        day["notes"] += f"\n\n{new_note}"
    else:
        day["notes"] = new_note

    write_markdown(file_path, data)
    print(f"Added note: {new_note[:32]}...")


def interactive_add_note(file_path: str) -> None:
    """Prompt the user for a note interactively."""
    note = input("Enter the note: ").strip()
    if not note:
        print("Note cannot be empty. Aborting.")
        return

    add_note(file_path, note)
