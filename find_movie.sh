################################################################################
# find_movie.sh
#
# Description:
#   This script searches for movie titles in a specified markdown file and allows
#   filtering and sorting based on options.
#
# Usage:
#   ./find_movie.sh [OPTIONS] MOVIE_TITLE
#
# Options:
#   -d, --date      Sort movies by date (year).
#   -y, --year YEAR Filter movies by the specified year.
#
# Example usage:
#   ./find_movie.sh "Batman"
#     - Searches for movies containing "Batman" in their titles.
#
#   ./find_movie.sh -d "Batman"
#     - Searches for movies containing "Batman" and sorts them by date.
#
#   ./find_movie.sh -y 2022 "Batman"
#     - Searches for movies containing "Batman" released in the year 2022.
#
# Notes:
#   - Movie titles must be listed in a markdown file named "movies.md" in the
#     "Notes" directory relative to the script.
#   - Output includes the number of movies found and lists them with highlighted
#     search terms (if available) or sorted by date (if -d option is used).
#
################################################################################

find_movie() {
    local sort_by_date=false
    local year_filter=""

    # Parse options
    while [[ "$1" =~ ^- ]]; do
        case "$1" in
            -d|--date)
                sort_by_date=true
                ;;
            -y|--year)
                shift
                year_filter="$1"
                ;;
            *)
                echo "Unknown option: $1"
                return 1
                ;;
        esac
        shift
    done

    local movie_name="$1"
    local movies_file="Notes/movies.md"
    local temp_file=$(mktemp)

    # Search for the movie with highlighted term
    grep --color=always -i "$movie_name" "$movies_file" > "$temp_file"

    # Filter by year if specified
    if [[ -n "$year_filter" ]]; then
        grep --color=always -i "($year_filter)" "$temp_file" > "${temp_file}.filtered"
        mv "${temp_file}.filtered" "$temp_file"
    fi

    # Count the number of movies found
    local count=$(wc -l < "$temp_file" | tr -d ' ')
    echo ""
    echo "Number of movies found: $count"
    echo ""

    if $sort_by_date; then
        # Extract year from the last set of parentheses, sort and keep the color
        awk -F'[()]' '{print $(NF-1), $0}' "$temp_file" | sort -k1,1n | cut -d' ' -f2-
    else
        # Print the found movies with highlighted term without sorting
        cat "$temp_file"
    fi

    # Clean up
    rm "$temp_file"
}
