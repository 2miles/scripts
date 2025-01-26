#!/bin/bash

################################################################################
# daily.sh
#
# Description:
#   This script manages daily notes in markdown format. It organizes tasks and 
#   notes by date and allows adding new tasks, notes, and editing the daily file.
#
# Usage:
#   ./daily.sh [OPTIONS]
#
# Options:
#   -t                Add a new checkbox under the "### Tasks" section for today.
#   -n                Add a new note under the "### Notes" section for today.
#   -o                Open the current month's markdown file in the default editor.
#
# Example usage:
#   ./daily.sh -t
#     - Prompts the user to enter text for a new checkbox and appends it to the 
#       "### Tasks" section for today.
#
#   ./daily.sh -n
#     - Prompts the user to enter a new note and appends it to the "### Notes" 
#       section for today.
#
#   ./daily.sh -o
#     - Opens the current month's markdown file in the default editor for manual 
#       editing.
#
# Notes:
#   - Daily notes are stored in the "$HOME/Notes/Daily" directory, organized by 
#     year and month.
#   - Each day's section begins with a date header ("## YYYY-MM-DD Day") followed 
#     by "### Tasks" and "### Notes" subsections.
#   - If the script is run on a new day, it will automatically create a new 
#     section for that day if it doesn't already exist.
#
################################################################################


# Define the base directory for notes
BASE_DIR="$HOME/Notes/Daily"

# Get the current date, year, month, and month name
CURRENT_DATE=$(date +%Y-%m-%d)
CURRENT_DAY=$(date +%a)
CURRENT_YEAR=$(date +%Y)
CURRENT_MONTH=$(date +%-m)
CURRENT_MONTH_NAME=$(date +%b | tr '[:upper:]' '[:lower:]')

# Define the file path for the current month
FILE="$BASE_DIR/$CURRENT_YEAR/${CURRENT_YEAR}_${CURRENT_MONTH}_${CURRENT_MONTH_NAME}.md"

# Ensure the directories and file exist
mkdir -p "$BASE_DIR/$CURRENT_YEAR"
touch "$FILE"

# Function to create a new section if it doesn't exist
create_new_day() {
  if ! grep -q "^## $CURRENT_DATE $CURRENT_DAY" "$FILE"; then
    echo "" >> "$FILE"
    echo "## $CURRENT_DATE $CURRENT_DAY" >> "$FILE"
    echo "" >> "$FILE"
    echo "### Tasks" >> "$FILE"
    echo "" >> "$FILE"
    echo "" >> "$FILE"
    echo "### Notes" >> "$FILE"
  fi
}

add_checkbox() {
  create_new_day  # Ensure today's section exists

  # Locate the line where the "### Tasks" section starts
  TASKS_LINE=$(grep -n "^### Tasks" "$FILE" | tail -n 1 | cut -d: -f1)

  if [ -z "$TASKS_LINE" ]; then
    # If "### Tasks" is missing for some reason, create it in today's section
    sed -i '' "/## $CURRENT_DATE $CURRENT_DAY/a\\
### Tasks\\
" "$FILE"
    TASKS_LINE=$(grep -n "^### Tasks" "$FILE" | tail -n 1 | cut -d: -f1)
  fi

  # Ensure a blank line before the new checkbox
  sed -i '' "${TASKS_LINE}a\\
\\
- [ ] $1" "$FILE"
}

# Function to add a new note under the Notes section
add_note() {
  create_new_day
  echo "" >> "$FILE"
  echo "$1" >> "$FILE"
}

# Parse command-line arguments
while getopts "tno" flag; do
  case "$flag" in
    t)
      echo -n "Enter the text for the new checkbox: "
      read -r CHECKBOX_TEXT
      add_checkbox "$CHECKBOX_TEXT"
      echo "Added a new unchecked checkbox with text.";;
    n)
      echo -n "Enter your note: "
      read -r NOTE
      add_note "$NOTE"
      echo "Added a new note.";;
    o)
      EDITOR=${EDITOR:-vim}
      $EDITOR "$FILE";;
    *)
      echo "Invalid option. Use -t, -n, or -o.";;
  esac
done

# If no flags are provided, show usage instructions
if [ $OPTIND -eq 1 ]; then
  echo "Usage: daily [-t | -n | -o]"
  echo "  -t: Add a new unchecked markdown checkbox to today's section"
  echo "  -n: Add a new note to today's section"
  echo "  -o: Open the file in the default editor"
fi
