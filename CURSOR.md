## Overview

This project scrapes Yu-Gi-Oh! Genesys Format point values from the official site, optionally enriching the results with card metadata from the YGOPRODeck API, and exports everything to JSON.

## Key Entry Points

- `scraper.py`: CLI for scraping. Supports `-g/--genesys` to export raw Genesys data or the default enriched dataset. `--output-path` lets users choose the target JSON file.
- `ygopro.py`: Helpers for talking to the YGOPRODeck API and matching card names (exact and fuzzy) against Genesys entries.

## Typical Workflow

1. Install dependencies via `uv sync`.
2. Run `uv run scraper.py` for enriched output (writes `genesys.json` by default).
3. Run `uv run scraper.py -g` to skip YGOPRO enrichment and capture Genesys-only data.

## Notable Details

- `scrape_genesys_data()` uses BeautifulSoup to parse the Genesys table.
- Fuzzy matching relies on RapidFuzz to tolerate naming differences across sources.
- Output is UTF-8 JSON with indentation for readability.

