from src.logic import Requirement, requirement_in_logic, requirements_in_logic
from src.state import State


def test_empty_requirement_valid():
    # Arrange
    state = State([])
    check = []

    # Act
    in_logic = requirements_in_logic(state, check)

    # Assert
    assert in_logic is True


def test_is_adult_requirement():
    # Arrange
    state = State([("isadult", 1, 0)])
    adult_requirement = Requirement(
        item="isadult", minimum_upgrade_level=1, exact_upgrade_level=True
    )
    child_requirement = Requirement(
        item="isadult", minimum_upgrade_level=0, exact_upgrade_level=True
    )

    # Act & Assert
    assert requirement_in_logic(state, adult_requirement) is False
    assert requirement_in_logic(state, child_requirement) is True
    state.change_age()
    assert requirement_in_logic(state, adult_requirement) is True
    assert requirement_in_logic(state, child_requirement) is False


def test_progressive_item():
    # Arrange
    state = State(items_pool=[("isadult", 1, 0), ("Progressive Hookshot", 2, 1)])
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
    state = State(items_pool=[("isadult", 1, 0), ("Progressive Hookshot", 2, 1)])
    adult = Requirement(
        item="isadult", minimum_upgrade_level=1, exact_upgrade_level=True
    )
    child = Requirement(
        item="isadult", minimum_upgrade_level=0, exact_upgrade_level=True
    )
    longshot = Requirement(item="Progressive Hookshot", minimum_upgrade_level=2)
    hookshot = Requirement(item="Progressive Hookshot", minimum_upgrade_level=1)

    # Act & Assert
    assert requirements_in_logic(state, [child, longshot]) is False
    assert requirements_in_logic(state, [child, hookshot]) is True
    assert requirements_in_logic(state, [adult, hookshot]) is False


# def test_5(self):
#     state = State(base_items=[])
#     mylogic = {"Impa at Castle": []}
#     state, logic=mylogic))
#
# def test_6(self):
#     state = State(
#         base_items=[("isadult", 1, 1), ("Progressive Hookshot", 2, 2)]
#     )
#     mylogic = {
#         "Gerudo Training Grounds Stalfos Chest": [
#             ("isadult", 1),
#             ("has_access|GTG", 1),
#         ]
#     }
#
#         logic.in_logic(state, logic=mylogic),
#         ["Gerudo Training Grounds Stalfos Chest"],
#     )
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
