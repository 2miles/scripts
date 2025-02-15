import calendar
import os
from datetime import datetime

# Base directory for notes
BASE_DIR = os.path.expanduser("~/Notes/Daily")


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_current_date_day():
    return datetime.now().strftime("%Y-%m-%d %a")


def get_current_year():
    return datetime.now().strftime("%Y")


def get_current_month():
    return datetime.now().strftime("%m")


def get_current_month_name():
    return datetime.now().strftime("%b").lower()


def get_prev_month_name() -> str:
    current_month = datetime.now().month  # Get the current month as an int
    if current_month == 1:  # If January, go to December
        prev_month = 12
    else:
        prev_month = current_month - 1
    return calendar.month_abbr[prev_month].lower()


def get_current_year_dir():
    return os.path.join(BASE_DIR, get_current_year())


# Ensure directory exists
os.makedirs(os.path.join(BASE_DIR, get_current_year()), exist_ok=True)


# Paths for storing notes and tasks
def get_file_path():
    year = get_current_year()
    return os.path.join(
        BASE_DIR,
        year,
        f"{year}_{get_current_month()}_{get_current_month_name()}.md",
    )


def get_json_file_path():
    year = get_current_year()
    return os.path.join(
        BASE_DIR,
        year,
        f"{year}_{get_current_month()}_{get_current_month_name()}.json",
    )


def get_prev_json_file_path() -> str:
    """
    Return the previous month's JSON file path if it exists.
    """
    current_year = int(get_current_year())
    current_month = int(get_current_month())

    if current_month == 1:  # If January, go to December of the previous year
        prev_year = current_year - 1
        prev_month = 12
    else:
        prev_year = current_year
        prev_month = current_month - 1

    prev_month_name = get_prev_month_name()

    prev_json_path = os.path.join(
        BASE_DIR,
        str(prev_year),
        f"{prev_year}_{str(prev_month).zfill(2)}_{prev_month_name}.json",
    )

    return prev_json_path if os.path.exists(prev_json_path) else None
