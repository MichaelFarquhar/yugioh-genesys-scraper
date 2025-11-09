# Yu-Gi-Oh! Genesys Format Scraper

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![UV](https://img.shields.io/badge/uv-30173d?style=for-the-badge&logo=uv&logoColor=DE5FE9)

A Python scraper that extracts Yu-Gi-Oh! Genesys Format card points data from the official website and saves it as JSON. This script scrapes the Genesys Format points table from the official Yu-Gi-Oh! website, extracting card names and their corresponding point values. The data is saved to `genesys.json` in a structured format for easy use.

## 📦 Installation

1. Ensure Python 3.8+ and UV are installed on your system.

2. Install dependencies using UV:

```bash
uv sync
```

## 🚀 Running Locally

After installing dependencies, run the scraper:

```bash
uv run scraper.py
```

This will create a `genesys.json` file in the base directory containing the scraped card data with full YGOPRO enrichment.

### Export Genesys Data Only

To export the raw Genesys data without the additional YGOPRO enrichment, use the `-g` (or `--genesys`) flag:

```bash
uv run scraper.py -g
```

Both commands accept an optional `--output-path` argument if you want to write to a different file.

## 🎴 Data Format

The scraper retrieves card information from the official Genesys Format website and, by default, enriches it with complete card data from the [YGOPRODeck API](https://ygoprodeck.com/api-guide/). Each entry in the enriched dataset contains:

### Top-Level Structure

```json
[
    {
        "card_name": "Abyss Dweller",
        "points": 100,
        "card_info": {
            /* See card_info structure below */
        }
    },
    {
        /* ... */
    }
]
```

### card_info Structure

```json
{
    "id": 21044178,
    "name": "Abyss Dweller",
    "typeline": ["Sea Serpent", "Xyz", "Effect"],
    "type": "XYZ Monster",
    "humanReadableCardType": "Xyz Effect Monster",
    "frameType": "xyz",
    "desc": "2 Level 4 monsters\nWhile this card has a material attached...",
    "race": "Sea Serpent",
    "atk": 1700,
    "def": 1400,
    "level": 4,
    "attribute": "WATER",
    "ygoprodeck_url": "https://ygoprodeck.com/card/abyss-dweller-1806",
    "card_sets": [
        {
            "set_name": "25th Anniversary Rarity Collection II",
            "set_code": "RA02-EN033",
            "set_rarity": "Secret Rare",
            "set_rarity_code": "(ScR)",
            "set_price": "0"
        }
    ],
    "banlist_info": {
        "ban_tcg": "Forbidden",
        "ban_ocg": "Forbidden"
    },
    "card_images": [
        {
            "id": 21044178,
            "image_url": "https://images.ygoprodeck.com/images/cards/21044178.jpg",
            "image_url_small": "https://images.ygoprodeck.com/images/cards_small/21044178.jpg",
            "image_url_cropped": "https://images.ygoprodeck.com/images/cards_cropped/21044178.jpg"
        }
    ],
    "card_prices": [
        {
            "cardmarket_price": "0.07",
            "tcgplayer_price": "0.09",
            "ebay_price": "1.75",
            "amazon_price": "1.68",
            "coolstuffinc_price": "1.99"
        }
    ]
}
```

If you run the scraper with `--genesys-only`, each record contains only the `card_name` and `points` fields.

## 🔗 YGOPro API Integration

This scraper automatically retrieves comprehensive card information from the YGOPRODeck API for each card found in the Genesys Format points table. The integration uses fuzzy matching to ensure cards are correctly matched between the two data sources, even when names have slight variations (such as spacing differences or special characters). Each card in the output includes the full `card_info` object from the YGOPro API, containing detailed information including card images, set information, prices, banlist status, and more.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.

## ⚠️ Disclaimer

This scraper is not malicious and is intended for legitimate use only. The data will be scraped approximately once a month when Genesys Format points values are updated on the official website. For information regarding the YGOPro API's rate limiting and usage rules, please refer to the [YGOPRODeck API Guide](https://ygoprodeck.com/api-guide/).
