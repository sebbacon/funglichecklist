import json
import csv

# Replace 'your_file.ldjson' with the path to your actual ldjson file
ldjson_file_path = "checklist.json"
output_csv_path = "synonyms_to_canonical.csv"


def process_ldjson_to_csv(ldjson_path, csv_path):
    processed = (
        set()
    )  # To keep track of processed synonym-canonical pairs to avoid duplicates

    with open(ldjson_path, "r") as infile, open(
        csv_path, "w", newline="", encoding="utf-8"
    ) as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(["Synonym", "Canonical Name"])  # Writing the header

        for line in infile:
            try:
                record = json.loads(
                    line
                )  # Parse each line of the ldjson file to a dictionary
                if not record["species_name"]:
                    print("Error", record)
                    continue
                canonical_name = record["species_name"]["name"]
                for synonym in record["synonyms"]:
                    synonym_name = synonym["name"]

                    # Check if synonym is not the canonical name and not already processed
                    if (
                        synonym_name != canonical_name
                        and (synonym_name, canonical_name) not in processed
                    ):
                        csv_writer.writerow([synonym_name, canonical_name])
                        processed.add(
                            (synonym_name, canonical_name)
                        )  # Mark this pair as processed
            except json.JSONDecodeError:
                print("Error decoding JSON from line:", line)
            except KeyError as e:
                print(f"Missing expected key {e} in line:", line)


import pandas as pd


def rootify(data):
    # Assuming `data` is your original DataFrame and `mapping` is the synonym to canonical name dictionary.

    def find_root_canonical_name(synonym, mapping, visited):
        if synonym not in mapping or synonym in visited:
            return [synonym]
        visited.add(synonym)
        return find_root_canonical_name(mapping[synonym], mapping, visited)

    # Convert the DataFrame to a dictionary for easier lookups.
    mapping = pd.Series(data["Canonical Name"].values, index=data["Synonym"]).to_dict()

    # Store the final root names for each synonym.
    synonym_to_roots = {}

    for synonym in mapping:
        synonym_to_roots[synonym] = find_root_canonical_name(
            mapping[synonym], mapping, set()
        )

    # Flatten the synonym_to_roots mapping to a list of synonym and root name pairs.
    flattened_data = [
        (synonym, root) for synonym, roots in synonym_to_roots.items() for root in roots
    ]

    # Create a DataFrame from the flattened data.
    flattened_df = pd.DataFrame(
        flattened_data, columns=["Synonym", "Root Canonical Name"]
    )

    # Define the path for the new CSV file.
    output_file_path = "flattened_synonyms_to_root_canonical.csv"

    # Write the DataFrame to a CSV file.
    flattened_df.to_csv(output_file_path, index=False)

    # The output_file_path variable contains the path to the generated CSV file.


# Call the function with your ldjson file path and desired output CSV file path
process_ldjson_to_csv(ldjson_file_path, output_csv_path)
rootify(pd.read_csv(output_csv_path))
