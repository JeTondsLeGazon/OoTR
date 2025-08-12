from typing import Callable
from mylog import logger
import json

from src.state import State
from pathlib import Path
from dataclasses import dataclass

# Free Scarecrow
# Automatic Bean plantation everywhere upon purchase
# Rupies not taken into account
# Time of day always favorable
# Skulltulas incrementely updated
# KZ skip, Mido skip, Reversed Wasteland are possible
# TODO: load logic according to settings, check randomizer repo. This whole file should not exist


@dataclass
class Requirement:
    item: str | None = None
    action: Callable | None = None
    minimum_upgrade_level: int = 0
    exact_upgrade_level: bool = False


MED_BRIDGE = 2

here = Path(__file__).parent
with open(here / ".." / "resources" / "dungeons_acess.json", "r") as f:
    dungeons_acess = json.load(f)


def bridge_open(nb_med_req, state):
    """
    Checks whether the bridge to GC is open according to Medallions.

    state(State): state of the player
    """
    return state.current_med() >= MED_BRIDGE


def is_where(zone, where):
    return zone == where


def has_spawn(zone, state):
    if state.items["isadult"]["current"] == 0:
        return zone == state.child_spawn
    else:
        return zone == state.adult_spawn


def has_access(zone, state) -> bool:
    """
    Checks the conditions to access particular zone given a state.

    zone(str): zone whose conditions of access will be evaluated.
    state(State): state of the player.
    """
    if zone == "Trials":
        return bridge_open(MED_BRIDGE, state)

    elif zone in dungeons_acess:
        if isinstance(dungeons_acess[zone][0], tuple):
            return requirements_in_logic(state, dungeons_acess[zone])
        else:
            return any(
                [requirements_in_logic(state, rr) for rr in dungeons_acess[zone]]
            )

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
        logger.error(f"Zone {zone} not found in has_access function")
        return False


def in_logic(state: State, logic: dict) -> list[str]:
    """
    Returns all checks that can be accessed according to played logic given a
    state.

    state(State): state of the player
    logic(dict): logic used
    """
    checks_in_logic = []
    for l, r in logic.items():
        if len(r) == 0:
            checks_in_logic.append(l)

        elif isinstance(r[0], tuple):  # Only one logic possible
            if requirements_in_logic(state, r):
                checks_in_logic.append(l)

        else:  # Many logics possible
            if any([requirements_in_logic(state, rr) for rr in r]):
                checks_in_logic.append(l)
    return checks_in_logic


def bool_logic(state: State, logic: dict) -> list[bool]:
    """
    Returns logic in the form of boolean array.
    """
    checks_in_logic = in_logic(state, logic)
    return [check in checks_in_logic for check in logic]


def requirements_in_logic(state: State, requirements: list[Requirement]) -> bool:
    return all(
        [requirement_in_logic(state, requirement) for requirement in requirements]
    )


def requirement_in_logic(
    state: State,
    requirement: Requirement,
) -> bool:
    """
    Returns whether or not the requirement is satisfied by the state or not.
    """
    if requirement.item is not None:
        minimum_upgrade_level = requirement.minimum_upgrade_level
        return (
            state.items[requirement.item].current_progression >= minimum_upgrade_level
            if not requirement.exact_upgrade_level
            else state.items[requirement.item].current_progression
            == minimum_upgrade_level
        )
    if requirement.action is None:
        return True

    return requirement.action(state)


def get_logic():
    with open("resources/logic.json", "r") as f:
        return json.load(f)


def get_additionnal_actions():
    with open("resources/additionnal_actions.json", "r") as f:
        return json.load(f)


def get_additionnal_logic(
    state: State,
):
    additional_actions = get_additionnal_actions()
    logic_array = []
    for r, _ in additional_actions.values():
        if len(r) == 0:
            logic_array.append(True)
        elif isinstance(r[0], tuple):
            logic_array.append(requirements_in_logic(state, r))
        else:
            logic_array.append(any([requirements_in_logic(state, rr) for rr in r]))
    return logic_array
