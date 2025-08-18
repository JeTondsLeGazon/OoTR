import pytest
from src.logic.utils import (
    Requirement,
    in_logic,
    requirement_in_logic,
    requirements_in_logic,
    has_access,
)
from functools import partial
from src.state import Item, State


def test_empty_requirement_valid():
    # Arrange
    state = State([])
    check = []

    # Act
    is_in_logic = requirements_in_logic(state, check)

    # Assert
    assert is_in_logic is True


def test_requirement_from_dict():
    # Arrange
    requirement_dict = {
        "item": "Progressive Hookshot",
        "minimum_upgrade_level": 1,
        "is_adult": False,
        "action": None,
    }

    # Act
    requirement = Requirement.from_dict(requirement_dict)

    # Assert
    assert requirement.item == "Progressive Hookshot"


def test_is_adult_requirement():
    # Arrange
    state = State([])
    state.set_age(0)
    adult_requirement = Requirement(
        is_adult=True,
    )
    child_requirement = Requirement(is_adult=False)

    # Act & Assert
    assert requirement_in_logic(state, adult_requirement) is False
    assert requirement_in_logic(state, child_requirement) is True
    state.change_age()
    assert requirement_in_logic(state, adult_requirement) is True
    assert requirement_in_logic(state, child_requirement) is False


def test_progressive_item():
    # Arrange
    state = State(items_pool=[("Progressive Hookshot", 2, 1)])
    hook_shot_level_0_requirement = Requirement(
        item="Progressive Hookshot", minimum_upgrade_level=0
    )
    hook_shot_level_1_requirement = Requirement(
        item="Progressive Hookshot", minimum_upgrade_level=1
    )
    hook_shot_level_2_requirement = Requirement(
        item="Progressive Hookshot", minimum_upgrade_level=2
    )

    # Act & Assert
    assert requirement_in_logic(state, hook_shot_level_0_requirement) is True
    assert requirement_in_logic(state, hook_shot_level_1_requirement) is True
    assert requirement_in_logic(state, hook_shot_level_2_requirement) is False
    state.item_update("Progressive Hookshot")
    assert requirement_in_logic(state, hook_shot_level_0_requirement) is True


def test_requirements_in_logic():
    # Arrange
    state = State(items_pool=[("Progressive Hookshot", 2, 1)])
    state.set_age(0)  # Set to child
    adult = Requirement(is_adult=True)
    child = Requirement(is_adult=False)
    longshot = Requirement(item="Progressive Hookshot", minimum_upgrade_level=2)
    hookshot = Requirement(item="Progressive Hookshot", minimum_upgrade_level=1)

    # Act & Assert
    assert requirements_in_logic(state, [child, longshot]) is False
    assert requirements_in_logic(state, [child, hookshot]) is True
    assert requirements_in_logic(state, [adult, hookshot]) is False


def test_current_nb_medallions():
    # Arrange
    state = State(items_pool=[])
    assert state.current_number_medallions() == 0

    # Act
    state.items["Forest Medallion"] = Item(
        name="Forest Medallion", max_progression=1, current_progression=1
    )

    # Asssert
    assert state.current_number_medallions() == 1


def test_in_logic():
    state = State(items_pool=[("Progressive Hookshot", 2, 2)])
    state.set_age(1)  # Set to adult
    mylogic = {
        "Gerudo Training Grounds Stalfos Chest": [
            [
                Requirement(is_adult=True),
                Requirement(action=partial(has_access, zone="GTG")),
            ],
        ]
    }

    assert in_logic(state, logic=mylogic) == ["Gerudo Training Grounds Stalfos Chest"]


@pytest.mark.parametrize(
    ("medallions", "access"),
    [
        ([("Forest Medallion", 1, 1)], False),
        (
            [
                ("Forest Medallion", 1, 1),
                ("Fire Medallion", 1, 1),
            ],
            True,
        ),
    ],
)
def test_trials_in_logic(medallions: list[tuple[str, int, int]], access: bool):
    # Arrange
    state = State(
        items_pool=[
            *medallions,
            ("Progressive Hookshot", 2, 2),
        ]
    )
    state.set_age(1)  # Set to adult
    mylogic = {
        "Ganons Castle Forest Trial Chest": [
            [
                Requirement(action=partial(has_access, "Trials")),
                Requirement(is_adult=True),
            ]
        ]
    }
    expected = ["Ganons Castle Forest Trial Chest"] if access else []

    # Act & Assert
    assert in_logic(state, logic=mylogic) == expected


def test_multi_logic():
    # Arrange
    state = State(
        items_pool=[
            ("Forest Medallion", 1, 1),
            ("Fire Medallion", 1, 1),
            ("Hover Boots", 1, 1),
        ]
    )
    state.set_age(1)  # Set to adult
    # For test purpose only, logic is wrong
    mylogic = {
        "Ganons Castle Forest Trial Chest": [
            [
                Requirement(action=partial(has_access, "Trials")),
                Requirement(is_adult=True),
                Requirement(item="Hover Boots", minimum_upgrade_level=1),
            ],
            [
                Requirement(action=partial(has_access, "Trials")),
                Requirement(is_adult=True),
                Requirement(item="Progressive Hookshotr", minimum_upgrade_level=2),
            ],
        ],
        "Ganons Castle Fire Trial Chest": [
            [
                Requirement(action=partial(has_access, "Trials")),
                Requirement(is_adult=True),
                Requirement(item="Hover Boots", minimum_upgrade_level=1),
            ],
        ],
        "Ganons Castle Water Trial Chest": [
            [
                Requirement(action=partial(has_access, "Trials")),
                Requirement(is_adult=True),
                Requirement(item="Progressive Hookshot", minimum_upgrade_level=2),
            ],
        ],
    }

    # Act & Assert
    assert in_logic(state, logic=mylogic) == [
        "Ganons Castle Forest Trial Chest",
        "Ganons Castle Fire Trial Chest",
    ]
