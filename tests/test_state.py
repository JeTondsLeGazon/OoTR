import pytest
from src.state import Item, State


@pytest.fixture
def items_pool() -> list[tuple[str, int, int]]:
    return [
        ("Sword", 3, 0),
        ("isadult", 1, 0),
        ("Light Arrow", 1, 0),
        ("Forest Medallion", 1, 0),
        ("Fire Medallion", 1, 0),
        ("Water Medallion", 1, 0),
        ("Spirit Medallion", 1, 0),
        ("Shadow Medallion", 1, 0),
        ("Light Medallion", 1, 0),
    ]


@pytest.fixture
def state(items_pool: list[tuple[str, int, int]]) -> State:
    return State(items_pool)


def test_item_update_progression():
    # Arrange
    item = Item("Sword", 3, 0)

    # Act & Assert
    item.update_progression()
    assert item.current_progression == 1

    item.update_progression()
    assert item.current_progression == 2

    item.update_progression()
    assert item.current_progression == 3

    with pytest.raises(ValueError):
        item.update_progression()


def test_state_initialization(state: State):
    # Assert
    assert state.items["Sword"].max_progression == 3
    assert state.items["Sword"].current_progression == 0
    assert state.items["isadult"].max_progression == 1
    assert state.items["isadult"].current_progression == 0


def test_item_update(state: State):
    # Arrange
    state.items["Sword"].current_progression = 0

    # Act
    state.item_update("Sword")

    # Assert
    assert state.items["Sword"].current_progression == 1


def test_item_update_invalid_item(state: State):
    # Act & Assert
    with pytest.raises(ValueError):
        state.item_update("Nonexistent Item")


def test_change_and_set_age(state: State):
    # Arrange
    state.set_age(0)  # Set to child
    assert state.is_adult is False

    # Act
    state.change_age()

    # Assert
    assert state.is_adult is True
    state.change_age()
    assert state.is_adult is False


def test_age_not_set():
    # Arrange
    state = State([])

    # Act & Assert
    with pytest.raises(ValueError):
        state.is_adult


def test_set_initial_items(state: State):
    # Arrange
    locations = {"starting_items": "Sword"}
    assert state.items["Sword"].current_progression == 0

    # Act
    state.set_initial_items(locations)

    # Assert
    assert state.items["Sword"].current_progression == 1


def test_current_number_medallions(state: State):
    # Arrange
    assert state.current_number_medallions() == 0
    state.item_update("Forest Medallion")
    state.item_update("Fire Medallion")

    # Act & Assert
    assert state.current_number_medallions() == 2


def test_can_beat_ganon(state: State):
    # Arrange
    assert not state.can_beat_ganon()

    # Give all medallions and Light Arrow
    for med in [
        "Forest Medallion",
        "Fire Medallion",
        "Water Medallion",
        "Spirit Medallion",
        "Shadow Medallion",
        "Light Medallion",
    ]:
        state.item_update(med)
    state.item_update("Light Arrow")

    # Act & Assert
    assert state.can_beat_ganon()
