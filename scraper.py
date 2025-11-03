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


def main():
    print("Scraping Genesys data...")
    data = scrape_genesys_data()
    
    print("Fetching YGOPro API data...")
    ygopro_data = fetch_ygopro_data()
    print(f"Fetched {len(ygopro_data)} cards from YGOPro API")
    
    print("Matching and enriching data...")
    enriched_data = match_and_enrich_genesys_data(data, ygopro_data)
    
    with open("genesys.json", "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully scraped {len(enriched_data)} cards to genesys.json")


if __name__ == "__main__":
    main()

