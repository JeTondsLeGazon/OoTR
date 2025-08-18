from __future__ import annotations
import json

from src.state import State
from pathlib import Path
from typing import Callable
import functools

from functools import partial

from dataclasses import dataclass

# Free Scarecrow
# Automatic Bean plantation everywhere upon purchase
# Rupies not taken into account
# Time of day always favorable
# Skulltulas incrementely updated
# KZ skip, Mido skip, Reversed Wasteland are possible
# TODO: load logic according to settings, check randomizer repo. This whole file should not exist
# TODO: check this variable
MED_BRIDGE = 2


@dataclass
class Requirement:
    item: str | None = None
    is_adult: bool | None = None
    action: Callable | None = None
    minimum_upgrade_level: int = 0
    exact_upgrade_level: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> Requirement:
        action_zone = data.get("action")
        callback = None
        if action_zone is not None:
            action, zone = action_zone.split("|")
            callback = possible_actions().get(action)
            if callback is None:
                raise ValueError(
                    f"Action '{data['action']}' not found in possible actions."
                )
            callback = partial(callback, zone)

        return cls(
            item=data.get("item"),
            is_adult=data.get("is_adult"),
            action=callback,
            minimum_upgrade_level=data.get("minimum_upgrade_level", 0),
            exact_upgrade_level=data.get("exact_upgrade_level", False),
        )


def in_logic(state: State, logic: dict[str, list[list[Requirement]]]) -> list[str]:
    """
    Returns all checks that can be accessed according to played logic given a
    state.
    """
    checks_in_logic = []
    for location, requirements_list in logic.items():
        if len(requirements_list) == 0:
            checks_in_logic.append(location)

        else:
            if any(
                [
                    requirements_in_logic(state, requirements)
                    for requirements in requirements_list
                ]
            ):
                checks_in_logic.append(location)
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
        if not state.items.get(requirement.item):
            return False
        return (
            state.items[requirement.item].current_progression >= minimum_upgrade_level
            if not requirement.exact_upgrade_level
            else state.items[requirement.item].current_progression
            == minimum_upgrade_level
        )

    if requirement.is_adult is not None:
        return state.is_adult == requirement.is_adult
    if requirement.action is None:
        return True

    return requirement.action(state=state)


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


@functools.lru_cache(maxsize=None)
def get_dungeons_requirements() -> dict[str, list[list[Requirement]]]:
    """
    Returns the dungeons requirements from the JSON file.
    """
    here = Path(__file__).parent
    with open(here.parent.parent / "resources" / "dungeons_access.json", "r") as f:
        dungeons_requirements_json = json.load(f)
    return {
        dungeon: [
            [Requirement.from_dict(req) for req in requirements]
            for requirements in requirements_list
        ]
        for dungeon, requirements_list in dungeons_requirements_json.items()
    }


def is_where(zone: str, state: State) -> bool:
    return zone == state.current_location


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

    elif zone in (dungeons_access := get_dungeons_requirements()):
        return any([requirements_in_logic(state, rr) for rr in dungeons_access[zone]])

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


def possible_actions() -> dict[str, Callable[[str, State], bool]]:
    return {
        "is_where": is_where,
        "has_spawn": has_spawn,
        "has_access": has_access,
    }
