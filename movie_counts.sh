#!/bin/bash

################################################################################
# movie_counts.sh
#
# Description:
#   This script iterates over the years 1900 to 2024 and uses the `find_movie.sh`
#   script to fetch the number of movies found for each year. The results are 
#   stored in a text file with the format "year: count".
#
# Usage:
#   ./movie_counts.sh
#     - This will loop through the years from 1900 to 2024, capture the movie 
#       count for each year using `find_movie.sh`, and save the results in 
#       "$HOME/Notes/movie_counts.txt".
#
# Notes:
#   - The script expects that `find_movie.sh` is available and executable in 
#     the "~/Scripts" directory.
#   - The script writes the results to "$HOME/Notes/movie_counts.txt".
#
################################################################################


output_file="$HOME/Notes/movie_counts.txt"

# Clear the output file before starting
> "$output_file"

# Loop through the years 1900 to 2024 and capture the output to extract the amount.
for year in $(seq 1900 2024); do
    # Capture the output and extract the amount
    output=$(~/Scripts/find_movie.sh -y "$year")
    count=$(echo "$output" | grep "Number of movies found" | awk '{print $5}')
    # Make sure count exists and is valid
    if [[ -z "$count" ]]; then
        count=0 
    fi
    echo "$year: $count" >> "$output_file"
done

echo "Results written to $output_file"
