################################################################################
# count_movies.sh
#
# Description:
#   This function counts the total number of movies listed in the "movies.md"
#   markdown file located in the "Notes" directory.
#
# Usage:
#   count_movies
#
# Notes:
#   - Assumes the existence of a markdown file named "movies.md" in the "Notes"
#     directory relative to the script.
#   - Outputs the total count of movies found in the file.
#
################################################################################

count_movies() {
    count=$(wc -l < Notes/movies.md)
    echo ""
    echo "Total number of movies: $count"
    echo ""
}
