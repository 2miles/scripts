#!/bin/bash

# -----------------------------------------------------------------------------
# Script Name: update_movies
# Description: This script compiles a list of movies from a NAS, downloads the 
#              list to a local machine, sorts, cleans, and converts the list to 
#              a Markdown format, and finally updates the local notes directory 
#              with the new list.
#
# Usage: 
#   ./update_movies
#
# Steps:
#   1. Compile Movie List on NAS:
#      - SSH into the NAS located at 192.168.0.2 with the username milesadmin.
#      - Navigate to the /volume1/data/media directory.
#      - Compile a list of movies from the animated, anime, movies, and 
#        documentaries directories.
#      - Save the compiled list as movies_new.md on the NAS.
#
#   2. Download the Movie List:
#      - Securely copy the movies_new.md file from the NAS to the ~/Downloads 
#        directory on your local machine.
#
#   3. Sort, Clean, and Convert to Markdown List Format:
#      - Navigate to the ~/Downloads directory.
#      - Sort the contents of movies_new.md and overwrite the file with the 
#        sorted contents.
#      - Use sed to clean and convert the file:
#          - Remove lines starting with ./.
#          - Remove lines starting with @ea.
#          - Remove any empty lines.
#          - Remove any text within square brackets ([ ]).
#          - Prefix each line with a hyphen (- ) to convert it to a Markdown 
#            list format.
#
#   4. Replace the Old Movie List in Your Notes:
#      - Move the processed movies_new.md to the ~/Notes directory.
#      - Navigate to the ~/Notes directory.
#      - Remove the old movies.md file.
#      - Rename movies_new.md to movies.md.
#
# Notes:
#   - Ensure that you have the necessary permissions to SSH into the NAS and 
#     access the specified directories.
#   - The script assumes that your NAS is reachable at 192.168.0.2 and that you 
#     have the correct username and credentials.
#   - Make sure that the sed command is compatible with the options used, as sed 
#     syntax can vary between different systems.
#
# Troubleshooting:
#   - If the script fails to SSH into the NAS, verify the NAS IP address, 
#     username, and your network connection.
#   - If the scp command fails, check the file path on the NAS and ensure that 
#     you have the necessary read permissions.
#   - If the sed command does not process the file correctly, check for any 
#     syntax issues or compatibility problems with your system's version of sed.
# -----------------------------------------------------------------------------

# Compile movie list on NAS
ssh milesadmin@192.168.0.2 'cd /volume1/data/media;
ls {./animated,./anime,./movies,./documentaries} > movies_new.md'

# Download the movie list
scp milesadmin@192.168.0.2:/volume1/data/media/movies_new.md ~/Downloads/

# Sort, clean, and convert to markdown list format
cd ~/Downloads
sort -o movies_new.md movies_new.md
sed -iE '/^\.\//d; /^@ea/d; /^$/d; s/ \[[^]]*\]//g; s/^/- /' movies_new.md

# Replace the old movie.md file in your notes with the new one
mv movies_new.md ~/Notes
cd ~/Notes
rm movies.md
mv movies_new.md movies.md
