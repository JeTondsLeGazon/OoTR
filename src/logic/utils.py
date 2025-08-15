from __future__ import annotations
from typing import Callable
import json

from src.state import State
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
    is_adult: bool | None = None
    action: Callable | None = None
    minimum_upgrade_level: int = 0
    exact_upgrade_level: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> Requirement:
        return cls(
            item=data.get("item"),
            is_adult=data.get("is_adult"),
            action=data.get("action"),
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
