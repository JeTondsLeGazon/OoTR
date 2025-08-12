from mylog import logger
import json

from state import State

# Free Scarecrow
# Automatic Bean plantation everywhere upon purchase
# Rupies not taken into account
# Time of day always favorable
# Skulltulas incrementely updated
# KZ skip, Mido skip, Reversed Wasteland are possible
# TODO: load logic according to settings, check randomizer repo. This whole file should not exist


MED_BRIDGE = 2


with open("resources/dungeons_access.json", "r") as f:
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


def requirements_in_logic(state, requirements, where=None) -> bool:
    """
    Returns whether the requirements list is fullfilled by state or not.

    state(State): state of the player
    requirement(list): list of requirements in the form of tuples.
    where(str): location of the player
    """
    try:
        for requirement, num in requirements:
            if not requirement_in_logic(state, requirement, num, where):
                return False
        return True
    except:
        logger.error(f"Set of requirements: {requirements} badly formated")
        return False


def requirement_in_logic(state, requirement, number, where=None) -> bool:
    """
    Returns if the requirement is fulfilled by the state or not.

    state(State): state of the player
    requirement(str): name of the status to check
    number(int or list): exact or minimum state number to return True
    where(str): location of the player
    """

    if requirement in state.items:
        if isinstance(number, int):
            return state.items[requirement]["current"] == number
        else:  # should be a list
            try:
                return state.items[requirement]["current"] >= number[0]
            except Exception as e:
                logger.error(
                    f"Unable to check requirement for check {requirement}due to {e}"
                )
                return False

    else:
        if "|" not in requirement:
            logger.error(f"Requirement {requirement} not in correct form")
            return False

        function_name, param = requirement.split("|")
        try:
            if function_name == "is_where":
                return is_where(param, where)
            else:
                return globals()[function_name](param, state)
        except Exception as e:
            logger.error(e)
            return False


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
