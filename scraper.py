import json
import requests
from bs4 import BeautifulSoup


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
    data = scrape_genesys_data()
    
    with open("genesys.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully scraped {len(data)} cards to genesys.json")


if __name__ == "__main__":
    main()

