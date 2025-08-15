from src.state import State
from src.logic.utils import requirements_in_logic, Requirement
from pathlib import Path
import json

MED_BRIDGE = 2

here = Path(__file__).parent
with open(here.parent.parent / "resources" / "dungeons_acess.json", "r") as f:
    dungeons_acess_json = json.load(f)
dungeon_access = {
    dungeon: [Requirement.from_json(**req) for req in requirements]
    for dungeon, requirements in dungeons_acess_json.items()
}


def is_where(zone: str, where: str) -> bool:
    return zone == where


def has_spawn(zone: str, state: State) -> bool:
    if state.is_adult:
        return zone == state.adult_spawn_location
    return zone == state.child_spawn_location


def _bridge_open(nb_med_req: int, state: State) -> bool:
    """
    Checks whether the bridge to GC is open according to Medallions.
    """
    return state.current_number_medallions() >= nb_med_req


def has_access(zone: str, state: State) -> bool:
    """
    Checks the conditions to access particular zone given a state.
    """
    if zone == "Trials":
        return _bridge_open(MED_BRIDGE, state)

    elif zone in dungeons_acess:
        return any([requirements_in_logic(state, rr) for rr in dungeons_acess[zone]])

    elif zone == "Biggoron":
        req = [
            [("Bolero of Fire", 1), ("Progressive Hookshot", [1]), ("isadult", 1)],
            [("Bolero of Fire", 1), ("Hover Boots", 1), ("isadult", 1)],
            [("Bomb Bag", 1), ("isadult", 1)],
            [("Bow", 1), ("isadult", 1)],
            [("Progressive Strength Upgrade", [1]), ("isadult", 1)],
            [("Megaton Hammer", 1), ("isadult", 1)],
            [("Dins Fire", 1), ("Magic Meter", 1), ("isadult", 1)],
            [("isadult", 1), ("has_spawn|DMC Upper", 1)],
        ]
        return any([requirements_in_logic(state, rr) for rr in req])

    else:
        print(f"Zone {zone} not found in has_access function")
        return False
