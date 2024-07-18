#!/bin/bash

################################################################################
# grow_list.sh
#
# Description:
#   This script takes a filename and a list of words as arguments and appends
#   the words to the specified file in markdown list format. If an argument
#   contains underscores (_), they will be replaced with spaces.
#
# Usage:
#   ./grow_list.sh FILE [WORD]...
#
# Example:
#   ./grow_list.sh myfile.txt word1 word2 two_words another_word
#     - Appends the words "word1", "word2", "two words", and "another word" to "myfile.txt".
#
################################################################################

# Function to display usage information
show_help() {
    cat << EOF
Usage: ./grow_list.sh FILE [WORD]...

Description:
  This script takes a filename and a list of words as arguments and appends
  the words to the specified file in markdown list format. If an argument
  contains underscores (_), they will be replaced with spaces.

Example:
  ./grow_list.sh myfile.txt word1 word2 two_words another_word
    - Appends the words "word1", "word2", "two words", and "another word" to "myfile.txt".
EOF
}

# Check for help option
if [[ "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# Check if there are at least two arguments (file + words)
if [[ "$#" -lt 2 ]]; then
    echo "Error: A file name and at least one word must be provided."
    show_help
    exit 1
fi

# Get the first argument as the file name
file="$1"

# Check if the file is a valid path and not a directory
if [[ -d "$file" ]]; then
    echo "Error: The specified file path is a directory."
    exit 1
fi

# Process each word argument starting from the second one
for word in "${@:2}"; do
    # Replace underscores with spaces
    formatted_word=$(echo "$word" | tr '_' ' ')
    # Append the formatted word to the file
    echo "- $formatted_word" >> "$file"
done

echo "Words appended to $file successfully."
