import matplotlib.pyplot as plt

# Path to your movie counts file
input_file = "/Users/miles/Notes/movie_counts.txt"
output_file = "/Users/miles/Notes/movie_counts_graph.png"

years = []
movie_counts = []

## Read into the arrays
with open(input_file, "r") as file:
    for line in file:
        year, count = line.strip().split(":")
        years.append(int(year))
        movie_counts.append(int(count))

# Ignore the first 20 years (skip the first 20 items in the lists)
years = years[20:]
movie_counts = movie_counts[20:]

# Create the bar graph
plt.figure(figsize=(15, 6))
plt.bar(years, movie_counts, color="skyblue")
plt.title("My Movies by Year", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Number of Movies", fontsize=14)
plt.xticks(years, rotation=90, fontsize=8)

# Bold every 10th label (decade years)
for i, label in enumerate(plt.gca().get_xticklabels()):
    year = int(label.get_text())
    if year % 10 == 0:
        label.set_fontweight("bold")

plt.tight_layout()
plt.savefig(output_file, dpi=300)  # Save as PNG
print(f"Bar graph saved as {output_file}")
