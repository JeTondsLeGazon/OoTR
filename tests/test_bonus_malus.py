from src.state import State
from src.bonus_malus import compute_malus
from src.bonus_malus import compute_bonus


import pytest


@pytest.mark.parametrize(
    "item_name, max_progression, current_progression, expected_bonus",
    [
        (
            "Progressive Hookshot",
            2,
            1,
            50,
        ),
        ("Progressive Hookshot", 2, 2, 0),  # Max progression reached, no bonus
        ("Nonexistent Item", 1, 0, 0),  # Nonexistent item should return 0 bonus
    ],
)
def test_bonus(
    item_name: str, max_progression: int, current_progression: int, expected_bonus: int
):
    # Arrange
    state = State(items_pool=[(item_name, max_progression, current_progression)])

    # Act
    bonus = compute_bonus(state, item_name)

    # Assert
    assert bonus == expected_bonus


@pytest.mark.parametrize(
    ("action, expected_malus"),
    [
        ("Shadow Temple Boss Key Chest", 40),
        ("Deliver RL", 5),
        ("Random action", 5),
    ],
)
def test_malus(action: str, expected_malus: int):
    # Arrange

    # Act
    malus = compute_malus(action)

    # Assert
    assert malus == expected_malus
