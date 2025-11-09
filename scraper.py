import argparse
import json
import re
import requests
from bs4 import BeautifulSoup
from ygopro import fetch_ygopro_data, match_and_enrich_genesys_data


def normalize_card_name(name):
    """Normalize card name by collapsing multiple spaces and removing spaces around hyphens."""
    if not name:
        return ""
    # First, remove spaces around hyphens (e.g., "K9- Lupis" -> "K9-Lupis", "K9 - Lupis" -> "K9-Lupis")
    normalized = re.sub(r'\s*-\s*', '-', name)
    # Then collapse multiple spaces into a single space, and strip leading/trailing whitespace
    normalized = re.sub(r'\s+', ' ', normalized.strip())
    return normalized


def scrape_genesys_data():
    url = "https://www.yugioh-card.com/en/genesys/"
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    
    if not table:
        raise ValueError("Table not found on the page")
    
    data = []
    rows = table.find_all("tr")[1:]
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 2:
            card_name = cells[0].get_text(strip=True)
            card_name = normalize_card_name(card_name)
            points_text = cells[1].get_text(strip=True)
            try:
                points = int(points_text)
            except ValueError:
                continue
            
            data.append({
                "card_name": card_name,
                "points": points
            })
    
    return data


def write_json(data, output_path):
    """Persist the provided dataset to disk."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def build_dataset(include_ygopro=True):
    """
    Scrape Genesys data and optionally enrich it with YGOPro details.

    Returns the dataset ready to be exported.
    """
    print("Scraping Genesys data...")
    genesys_data = scrape_genesys_data()

    if not include_ygopro:
        print("Skipping YGOPro API enrichment; exporting Genesys data only.")
        return genesys_data

    print("Fetching YGOPro API data...")
    ygopro_data = fetch_ygopro_data()
    print(f"Fetched {len(ygopro_data)} cards from YGOPro API")

    print("Matching and enriching data...")
    enriched_data = match_and_enrich_genesys_data(genesys_data, ygopro_data)
    print(f"Successfully matched {len(enriched_data)} cards with YGOPro data")

    return enriched_data


def parse_arguments():
    """Parse CLI arguments for exporting datasets."""
    parser = argparse.ArgumentParser(
        description="Scrape Yu-Gi-Oh! Genesys data and export it as JSON."
    )
    parser.add_argument(
        "-g",
        "--genesys",
        dest="genesys_only",
        action="store_true",
        help="Export only the Genesys data without YGOPro enrichment.",
    )
    parser.add_argument(
        "--output-path",
        default="genesys.json",
        help="Path for the exported JSON file (default: genesys.json).",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    include_ygopro = not args.genesys_only

    dataset = build_dataset(include_ygopro=include_ygopro)
    write_json(dataset, args.output_path)

    print(f"Successfully saved {len(dataset)} cards to {args.output_path}")


if __name__ == "__main__":
    main()

