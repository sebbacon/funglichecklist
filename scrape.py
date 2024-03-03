import requests
import os
import re

# Ensure data directory exists
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

base_url = "https://basidiochecklist.science.kew.org/BritishFungi/GBCHKLST/gbsyns.asp?intGBNum="


def find_latest_file_number(directory):
    """Find the highest number from the filenames in the given directory."""
    max_num = 0
    for filename in os.listdir(directory):
        match = re.search(r"page_(\d+).html", filename)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    return max_num


current_gbnum = find_latest_file_number(data_dir)
no_data_count = 0

while no_data_count <= 25:
    response = requests.get(f"{base_url}{current_gbnum}")
    content = response.content.decode("utf-8", "replace")

    if "No records found" in content:
        no_data_count += 1
    else:
        no_data_count = 0  # Reset counter if data is found
        # Write corrected content to a file
        with open(
            f"{data_dir}/page_{current_gbnum}.html", "w", encoding="utf-8"
        ) as file:
            file.write(content)

    if no_data_count > 25:
        break  # Exit loop if no data found in 25 consecutive pages

    current_gbnum += 1  # Move to the next page
    print(current_gbnum)
print("Scraping completed.")
