from __future__ import annotations
from dataclasses import dataclass
import logging
from typing import Dict, List
import random
import sys

# Built-ins
import fab_cards
import fabrary

# Set up Logging, I prefer to do this per script atm

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)


def build_power_list(fabrary_data: Dict) -> List[int]:
    """
    Import a Fabrary Dec, look up the corresponding card from the FAB Card JSON and return a list of attack values for
    every card in the deck.
    """
    cards = fab_cards.load_all_cards()
    power_values = []
    for card in fabrary_data["data"]["getDeck"]["deckCards"]:
        if "Equipment" in card["card"]["types"] or "Weapon" in card["card"]["types"]:
            continue
        if card["quantity"] < 1:
            continue

        found_card = fab_cards.find_card_with_name_and_pitch(
            cards=cards, name=card["card"]["name"], pitch=str(card["card"]["pitch"])
        )
        if found_card:
            for x in range(0, card["quantity"]):
                power_values.append(found_card["power"])
    return power_values


def sim_game_with_clashes(deck_1, deck_2):
    p1_wins = 0
    p2_wins = 0
    random.shuffle(deck_1)
    random.shuffle(deck_2)
    # First draw four cards each to start the game
    del deck_1[:4]
    del deck_2[:4]
    while True:
        # CLASH!
        if deck_1[0] > deck_2[0]:
            p1_wins += 1
        elif deck_2[0] > deck_1[0]:
            p2_wins += 1

        # Pretend we played some reasonable hands each
        p1_played = random.randint(1, 4)
        p2_played = random.randint(1, 4)
        del deck_1[:p1_played]
        del deck_2[:p2_played]
        # Then redraw
        del deck_1[: 4 - p1_played]
        del deck_2[: 4 - p2_played]

        if len(deck_1) == 0 or len(deck_2) == 0:
            return p1_wins, p2_wins


@dataclass
class ClashPlayer:
    name: str
    power_levels: List[int]

    @staticmethod
    def new(fabrary_json_filename: str) -> ClashPlayer:
        fabrary_data = fabrary.load_graphql_result(fabrary_json_filename)
        power_levels = build_power_list(fabrary_data)
        return ClashPlayer(name=fabrary_data["data"]["getDeck"]["name"], power_levels=power_levels)


player1 = ClashPlayer.new(fabrary_json_filename="./cache/deck1.json")
player2 = ClashPlayer.new(fabrary_json_filename="./cache/deck2.json")

p1_total_clashes = 0
p2_total_clashes = 0
NUM_GAMES = 10_000
for _ in range(0, 10_000):
    p1_wins, p2_wins = sim_game_with_clashes(player1.power_levels.copy(), player2.power_levels.copy())
    if p1_wins > p2_wins:
        p1_total_clashes += p1_wins
    elif p2_wins > p1_wins:
        p2_total_clashes += p2_wins

print("But what if we clashed 🥺👉👈?")
print(f"Running {NUM_GAMES} games...")
print(f"Total Clashes:  {p1_total_clashes + p2_total_clashes}")
print("-" * 40)
print(round(p1_total_clashes / (p1_total_clashes + p2_total_clashes) * 100, 2), "%:", player1.name)
print(round(p2_total_clashes / (p1_total_clashes + p2_total_clashes) * 100, 2), "%:", player2.name)
