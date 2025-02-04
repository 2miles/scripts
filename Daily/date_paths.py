import os
from datetime import datetime

# Base directory for notes
BASE_DIR = os.path.expanduser("~/Notes/Daily")


# Function to get the current date/time dynamically
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_current_date_day():
    return datetime.now().strftime("%Y-%m-%d %a")


def get_current_year():
    return datetime.now().strftime("%Y")


def get_current_month():
    return datetime.now().strftime("%m")  # Always zero-padded


def get_current_month_name():
    return datetime.now().strftime("%b").lower()


def get_current_year_dir():
    return os.path.join(BASE_DIR, get_current_year())


# Ensure directory exists
os.makedirs(os.path.join(BASE_DIR, get_current_year()), exist_ok=True)


# Paths for storing notes and tasks
def get_file_path():
    return os.path.join(
        BASE_DIR,
        get_current_year(),
        f"{get_current_year()}_{get_current_month()}_{get_current_month_name()}.md",
    )


def get_json_file_path():
    return os.path.join(
        BASE_DIR,
        get_current_year(),
        f"{get_current_year()}_{get_current_month()}_{get_current_month_name()}.json",
    )
