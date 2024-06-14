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
    count=$(grep -ci "$1" Notes/Idioms.md)
    echo ""
    echo "Number of idioms found: $count"
    echo ""
    grep -i "$1" Notes/Idioms.md
}
