import argparse
import json
from collections import namedtuple

PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])


def main(product_data, include_tags, exclude_tags):
    """
    The implementation of the pipeline test.
    Assumptions:
     - Input validation is being handled external to this function
     - We don't need to apply any kind of transformations to the data (e.g. sorting)
    """
    # Use a dictionary for matches to take advantage of hash lookups
    matches = {}
    for product in product_data:
        # Filter out products that don't match ANY of the include tags or do match ANY of the exclude tags
        # Avoiding standard any/all functions here because they check every element in the list before returning
        if set(include_tags).isdisjoint(product["tags"]) or not set(exclude_tags).isdisjoint(product["tags"]):
            continue
        
        # Append product code to the list of codes matched for a given product type
        matches[product["name"]] = [product["code"]] if product["name"] not in matches else matches[product["name"]] + [product["code"]]
    # Map the matches dictionary to a list of PreferenceMatch objects
    formattedMatches = [PreferenceMatch(name, codes) for name, codes in matches.items()]
    return formattedMatches


if __name__ == "__main__":

    def parse_tags(tags):
        return [tag for tag in tags.split(",") if tag]

    parser = argparse.ArgumentParser(
        description="Extracts unique product names matching given tags."
    )
    parser.add_argument(
        "product_data",
        help="a JSON file containing tagged product data",
    )
    parser.add_argument(
        "--include",
        type=parse_tags,
        help="a comma-separated list of tags whose products should be included",
        default="",
    )
    parser.add_argument(
        "--exclude",
        type=parse_tags,
        help="a comma-separated list of tags whose matching products should be excluded",
        default="",
    )

    args = parser.parse_args()

    with open(args.product_data) as f:
        product_data = json.load(f)

    order_items = main(product_data, args.include, args.exclude)

    for item in order_items:
        print("%s:\n%s\n" % (item.product_name, "\n".join(item.product_codes)))
