from bs4 import BeautifulSoup
import glob
import json
import re


def extract_species_name(soup):
    # Extracting the species name based on the first occurrence of italicized text within a bold tag
    name_element = soup.find(lambda tag: tag.name == "i" and tag.find_parent("b"))
    if name_element:
        return name_element.get_text(strip=True)
    return "Species name not found"


def extract_name_and_reference(soup):
    # Find all <b> tags that contain <i> tags
    b_tags = soup.find_all("b")
    for b_tag in b_tags:
        i_tag = b_tag.find("i")
        if i_tag:
            name = i_tag.get_text(strip=True)
            # Remove the <i> tag to help isolate the reference
            i_tag.extract()
            # Now, the reference is the remaining text in the <b> tag
            reference = b_tag.get_text(strip=True)
            return {"name": name, "reference": reference}


def extract_taxonomy(soup):
    # Find all <b> tags, then filter those containing commas and select the last one
    b_tags_with_commas = [tag for tag in soup.find_all("b") if "," in tag.get_text()]
    if b_tags_with_commas:
        last_b_tag = b_tags_with_commas[-1]
        taxonomy_text = last_b_tag.get_text(strip=True)
        taxonomy_parts = taxonomy_text.split(", ")
        taxonomy_levels = ["family", "order", "class", "phylum", "kingdom"]
        taxonomy = {}
        for level in taxonomy_levels:
            try:
                taxonomy[level] = taxonomy_parts.pop()
            except IndexError:
                taxonomy[level] = None
        return taxonomy
    return "Taxonomy information not found"


# Bad ones
# Synonyms:$ awk -F, '{print $1}' synonyms_to_canonical.csv  | sort | uniq -c | sort -g | grep -v " 1 "


def extract_synonyms(soup):
    synonyms = []
    # Find the first <p> tag whose first child is an <i> tag
    p_tag_with_i = soup.find(
        lambda tag: tag.name == "p" and tag.contents and tag.contents[0].name == "i"
    )
    if p_tag_with_i:
        items = p_tag_with_i.decode_contents().split("<br/>")
        for item in items:
            item_soup = BeautifulSoup(item, "html.parser")
            i_tag = item_soup.find("i")
            if i_tag:
                name = i_tag.get_text(strip=True)
                i_tag.extract()  # Remove the <i> tag to isolate the reference
                reference = item_soup.get_text(strip=True)
                synonyms.append({"name": name, "reference": reference})
    return synonyms


# Load the HTML content
number = 1
for page in glob.glob("data/*html"):
    with open(page, "r") as f:
        soup = BeautifulSoup(f, "html.parser")
        numbers = re.findall(r"\d+", page)

        # Extract the first (and in this case, only) group of digits found
        number_part = numbers[0] if numbers else None
        # Extract the required information
        species_name_and_reference = extract_name_and_reference(soup)
        taxonomy = extract_taxonomy(soup)
        synonyms = extract_synonyms(soup)

        # Assemble the results
        results = {
            "id": number_part,
            "species_name": species_name_and_reference,
            "taxonomy": taxonomy,
            "synonyms": synonyms,
        }
        number += 1

        print(json.dumps(results))
