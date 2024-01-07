"""
Helpers for parsing the Flesh and Blood Cards Github Repo.

https://github.com/the-fab-cube/flesh-and-blood-cards

The card JSON data is cached locally since it's several megs in size.
"""
from typing import Dict
import logging
import json
import os.path
import urllib.request

CARD_JSON_FILE = "./cache/card.json"


def update_card_json_cache():
    """Downloads the most recent card json into the cache."""
    logging.info("Downloading new Flesh and Blood Card JSON...")
    urllib.request.urlretrieve(
        url="https://raw.githubusercontent.com/the-fab-cube/flesh-and-blood-cards/develop/json/english/card.json",
        filename=CARD_JSON_FILE,
    )
    logging.info("Card JSON download complete.")


def load_all_cards() -> Dict:
    if not os.path.isfile(CARD_JSON_FILE):
        logging.info("Card JSON not found. Requesting Cache update...")
        update_card_json_cache()
    with open(CARD_JSON_FILE, encoding="utf-8", errors="ignore") as json_data:
        return json.load(json_data, strict=False)


def find_card_with_name_and_pitch(cards: Dict, name: str, pitch: str):
    found_card = next(c for c in cards if c["name"] == name and str(c["pitch"]) == str(pitch))
    return found_card
