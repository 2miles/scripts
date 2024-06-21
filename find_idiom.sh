################################################################################
# find_idiom.sh
#
# Description:
#   This function searches for idioms containing a specified keyword in the
#   "Idioms.md" markdown file located in the "Notes" directory. It counts and
#   displays the matching idioms along with their occurrences.
#
# Usage:
#   find_idiom KEYWORD
#
# Arguments:
#   KEYWORD   The keyword to search for within the idioms.
#
# Notes:
#   - Assumes the existence of a markdown file named "Idioms.md" in the "Notes"
#     directory relative to the script.
#   - Outputs the number of idioms found containing the keyword and lists them.
#
################################################################################

find_idiom() {
    local idioms_file="$HOME/Notes/idioms.md"

    # Check if the keyword argument is provided
    if [ -z "$1" ]; then
        echo "Usage: find_idiom KEYWORD"
        return 1
    fi

    # Check if the idioms file exists
    if [ ! -f "$idioms_file" ]; then
        echo "Error: $idioms_file not found."
        return 1
    fi

    local count=$(grep -ci "$1" "$idioms_file")
    echo ""
    echo "Number of idioms found: $count"
    echo ""
    grep -i "$1" "$idioms_file"
}

# Check if the script is being run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    find_idiom "$@"
fi
