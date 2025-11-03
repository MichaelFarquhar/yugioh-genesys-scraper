import requests
import re
import html
from rapidfuzz import fuzz, process


def normalize_name(name):
    """
    Normalize card names for matching by:
    - Decoding HTML entities (e.g., &amp; -> &)
    - Lowercasing
    - Removing all spaces, hyphens, and special characters
    - Handling Unicode characters properly
    """
    if not name:
        return ""
    
    # Decode HTML entities (e.g., &amp; -> &, &quot; -> ")
    normalized = html.unescape(name)
    
    # Lowercase
    normalized = normalized.lower()
    
    # Remove all whitespace (spaces, tabs, etc.)
    normalized = re.sub(r'\s+', '', normalized)
    
    # Remove hyphens and other common separators
    normalized = re.sub(r'[-_]+', '', normalized)
    
    # Remove all remaining special characters, keeping only alphanumeric and Unicode word characters
    # This preserves characters like Ø but removes punctuation
    normalized = re.sub(r'[^\w]', '', normalized, flags=re.UNICODE)
    
    return normalized


def fetch_ygopro_data():
    """Fetch all card data from YGOPro API."""
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    return data.get("data", [])


def create_name_map(ygopro_data):
    """
    Create mappings of normalized names to YGOPro card objects.
    Returns both exact match map and a list of normalized names for fuzzy matching.
    """
    name_map = {}
    normalized_names = []
    
    for card in ygopro_data:
        card_name = card.get("name", "")
        normalized = normalize_name(card_name)
        # Store the full card object
        name_map[normalized] = card
        normalized_names.append(normalized)
    
    return name_map, normalized_names


def find_fuzzy_match(query_name, normalized_names, name_map, threshold=85):
    """
    Find the best fuzzy match for a query name.
    Returns the matched card object if similarity is above threshold, None otherwise.
    """
    # Use rapidfuzz to find the best match
    result = process.extractOne(
        query_name,
        normalized_names,
        scorer=fuzz.WRatio,  # Weighted ratio works well for card names
        score_cutoff=threshold
    )
    
    if result:
        matched_name, score, _ = result
        return name_map[matched_name], score
    return None, 0


def match_and_enrich_genesys_data(genesys_data, ygopro_data):
    """
    Match genesys data with ygopro data and add card_info property.
    Uses exact matching first, then fuzzy matching as fallback.
    """
    name_map, normalized_names = create_name_map(ygopro_data)
    enriched_data = []
    unmatched_cards = []
    fuzzy_matched_cards = []
    
    for card in genesys_data:
        card_name = card.get("card_name", "")
        normalized_card_name = normalize_name(card_name)
        matched_card = None
        
        # Try exact match first
        if normalized_card_name in name_map:
            matched_card = name_map[normalized_card_name]
        else:
            # Try fuzzy matching
            fuzzy_match, similarity_score = find_fuzzy_match(
                normalized_card_name,
                normalized_names,
                name_map,
                threshold=85
            )
            
            if fuzzy_match:
                matched_card = fuzzy_match
                fuzzy_matched_cards.append((card_name, similarity_score))
                print(f"FUZZY MATCH: '{card_name}' matched with {similarity_score:.1f}% similarity")
            else:
                unmatched_cards.append(card_name)
                print(f"ERROR: No match found for card: {card_name}")
        
        if matched_card:
            # Add the card_info property with the full YGOPro object
            enriched_card = {
                "card_name": card_name,
                "points": card.get("points"),
                "card_info": matched_card
            }
            enriched_data.append(enriched_card)
    
    if fuzzy_matched_cards:
        print(f"\nTotal fuzzy matched cards: {len(fuzzy_matched_cards)}")
    
    if unmatched_cards:
        print(f"\nTotal unmatched cards: {len(unmatched_cards)}")
        print("Unmatched card names:")
        for unmatched in unmatched_cards:
            print(f"  - {unmatched}")
    
    return enriched_data

