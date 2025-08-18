from src.state import State
import functools
import json
from pathlib import Path

"""
Items and actions bonus and malus.

A malus represents the time lost when moving to the location.
A bonus represents some imaginary points that help the player to progress in the game.
"""

here = Path(__file__).parent


@functools.lru_cache(maxsize=None)
def get_bonuses() -> dict[str, int]:
    with open(here.parent / "resources" / "bonus.json", "r") as f:
        return json.load(f)


# TODO: is there malus from moving to one zone to another or just from 1 check to another ?
@functools.lru_cache(maxsize=None)
def get_maluses() -> dict[str, int]:
    with open(here.parent / "resources" / "malus.json", "r") as f:
        return json.load(f)


def compute_bonus(state: State, item_found: str) -> int:
    """
    Computes the bonus associated with the item found and the current state.
    """
    items_bonus = get_bonuses()

    if item_found not in items_bonus:
        return 0

    if (
        state.items[item_found].current_progression
        == state.items[item_found].max_progression
    ):
        return 0
    return items_bonus[item_found]


basic_malus = 5


def compute_malus(action: str) -> int:
    """
    Computes the malus associated with the action chosen and the current state.
    """
    malus = get_maluses()
    return malus.get(action, basic_malus)
