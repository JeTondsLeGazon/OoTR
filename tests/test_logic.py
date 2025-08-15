from src.logic.utils import (
    Requirement,
    in_logic,
    requirement_in_logic,
    requirements_in_logic,
)
from functools import partial
from src.logic.callbacks import has_access
from src.state import Item, State


def test_empty_requirement_valid():
    # Arrange
    state = State([])
    check = []

    # Act
    is_in_logic = requirements_in_logic(state, check)

    # Assert
    assert is_in_logic is True


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


#
# def test_7(self):
#     state = State(
#         base_items=[("isadult", 1, 1), ("Progressive Hookshot", 2, 2)]
#     )
#     mylogic = {
#         "Ganons Castle Forest Trial Chest": [
#             ("has_access|Trials", 1),
#             ("isadult", 1),
#         ]
#     }
#     state, logic=mylogic))
#
# def test_8(self):
#     state = State(
#         base_items=[
#             ("isadult", 1, 1),
#             ("Forest Medallion", 1, 1),
#             ("Fire Medallion", 1, 1),
#             ]
#         )
#         mylogic = {
#             "Ganons Castle Forest Trial Chest": [
#                 ("has_access|Trials", 1),
#                 ("isadult", 1),
#             ]
#         }
#
#             logic.in_logic(state, logic=mylogic), ["Ganons Castle Forest Trial Chest"]
#         )
#
# def test_9(self):
#     state = State(
#         base_items=[
#             ("isadult", 1, 1),
#             ("Forest Medallion", 1, 0),
#             ("Fire Medallion", 1, 1),
#         ]
#     )
#     mylogic = {
#         "Ganons Castle Forest Trial Chest": [
#             ("has_access|Trials", 1),
#             ("isadult", 1),
#         ]
#     }
#
#         logic.in_logic(state, logic=mylogic), ["Ganons Castle Forest Trial Chest"]
#     )
#
# def test_10(self):
#     state = State(base_items=[("isadult", 1, 1), ("Zeldas Lullaby", 1, 1)])
#     mylogic = {
#         "Song at Windmill": [("isadult", 1)],
#         "Song from Composer Grave": [("Zeldas Lullaby", 1)],
#         "Sheik in Crater": [("has_access|Fire", 1)],
#         "Song from Malon": [("isadult", 0)],
#         "Sheik in Ice Cavern": [
#             [("isadult", 1), ("Rutos Letter", 2), ("Zeldas Lullaby", 1)],
#             [("isadult", 1), ("Rutos Letter", 2), ("Hover Boots", 1)],
#         ],
#         "Kokiri Sword Chest": [("isadult", 0)],
#     }
#
#         logic.in_logic(state, logic=mylogic),
#         ["Song at Windmill", "Song from Composer Grave"],
#     )
#
#
