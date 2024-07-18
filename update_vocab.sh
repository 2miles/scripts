#!/bin/bash

################################################################################
# update_vocab.sh
#
# Description:
#   This script reads a markdown file containing a list of vocabulary words,
#   capitalizes the first letter of each word, sorts them alphabetically, and
#   removes duplicates.
#
# Usage:
#   ./update_vocab.sh [--help]
#
# Options:
#   --help    Display this help message.
#
# Notes:
#   - The vocabulary words must be listed in a markdown file named "vocabulary.md"
#     in the "Notes" directory relative to the user's home directory.
#   - The file format should be:
#     - word1
#     - word2
#     - word3
#
################################################################################

show_help() {
    cat << EOF
Usage: ./update_vocab.sh [--help]

Options:
  --help    Display this help message.

Description:
  This script reads a markdown file containing a list of vocabulary words,
  capitalizes the first letter of each word, sorts them alphabetically, and
  removes duplicates.

Notes:
  - The vocabulary words must be listed in a markdown file named "vocabulary.md"
    in the "Notes" directory relative to the user's home directory.
  - The file format should be:
    - word1
    - word2
    - word3
EOF
}

update_vocab() {
    local vocab_file="$HOME/Notes/vocabulary.md"
    local temp_file=$(mktemp)

    # Check if the vocabulary file exists
    if [[ ! -f "$vocab_file" ]]; then
        echo "Vocabulary file not found: $vocab_file"
        return 1
    fi

    # Read, capitalize the first letter of each word, sort, and remove duplicates
    awk '/^- /{print "- " toupper(substr($0, 3, 1)) tolower(substr($0, 4))}' "$vocab_file" | sort -u > "$temp_file"

    # Overwrite the original file with the processed content
    mv "$temp_file" "$vocab_file"

    echo "Vocabulary updated successfully."
}

# Parse options
if [[ "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# Execute the function if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    update_vocab
fi

