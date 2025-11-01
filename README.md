# Yu-Gi-Oh! Genesys Scraper

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

A Python scraper that extracts Yu-Gi-Oh! Genesys card points data from the official website and saves it as JSON.

## Description

This script scrapes the Genesys points table from the official Yu-Gi-Oh! website, extracting card names and their corresponding point values. The data is saved to `genesys.json` in a structured format for easy use.

## Installation

1. Ensure Python 3.8+ and UV are installed on your system.

2. Install dependencies using UV:

```bash
uv sync
```

## Running Locally

After installing dependencies, run the scraper:

```bash
uv run scraper.py
```

This will create a `genesys.json` file in the base directory containing the scraped card data.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This scraper is not malicious and is intended for legitimate use only. The data is scraped approximately once a month when Genesys points values are updated on the official website.
