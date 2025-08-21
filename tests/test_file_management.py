from pathlib import Path
import pytest
from src.spoiler_logs.files_management import (
    extract_locations_from_spoiler_logs,
    extract_age_from_spoiler_logs,
    extract_spawn_from_spoiler_logs,
    extract_data_from_spoiler_logs,
    load_spoiler_logs,
)


def test_extract_locations_from_spoiler_logs():
    # Arrange
    spoiler_logs = [
        {"locations": {"Location1": "Item1", "Location2": "Item2"}},
        {"locations": {"Location3": "Item3"}},
    ]
    expected = [
        {"Location1": "Item1", "Location2": "Item2"},
        {"Location3": "Item3"},
    ]

    # Act / Assert
    assert extract_locations_from_spoiler_logs(spoiler_logs) == expected


def test_extract_locations_error_if_not_all_logs_have_locations():
    # Arrange
    spoiler_logs = [
        {"locations": {"Location1": "Item1"}},
        {},
    ]

    # Act / Assert
    with pytest.raises(ValueError):
        extract_locations_from_spoiler_logs(spoiler_logs)


def test_extract_age():
    # Arrange
    spoiler_logs = [
        {"randomized_settings": {"starting_age": "child"}},
        {"randomized_settings": {"starting_age": "adult"}},
    ]
    expected = [0, 1]

    # Act / Assert
    assert extract_age_from_spoiler_logs(spoiler_logs) == expected


def test_extract_age_default_value():
    # Arrange
    spoiler_logs = [
        {"randomized_settings": {}},
        {"randomized_settings": {"starting_age": "adult"}},
    ]
    expected = [1, 1]  # Default is adult if not specified

    # Act / Assert
    assert extract_age_from_spoiler_logs(spoiler_logs) == expected


def test_extract_spawn():
    # Arrange
    spoiler_logs = [
        {
            "entrances": {
                "Child Spawn -> KF Links House": {"region": "Kokiri Forest"},
                "Adult Spawn -> Temple of Time": {"region": "Temple of Time"},
            }
        },
        {
            "entrances": {
                "Child Spawn -> wrong": {"region": "Deku Tree"},
                "Adult Spawn -> Temple of Time": {"region": "Temple of Time"},
            }
        },
        {
            "entrances": {
                "Child Spawn -> KF Links House": "Deku Tree",
                "Adult Spawn -> Temple of Time": {"region": "Temple of Time"},
            }
        },
    ]
    expected = [
        ("Kokiri Forest", "Temple of Time"),
        (None, "Temple of Time"),
        ("Deku Tree", "Temple of Time"),
    ]

    # Act / Assert
    assert extract_spawn_from_spoiler_logs(spoiler_logs) == expected


def test_load_spoiler_logs(resources: Path):
    # Arrange
    paths = list(resources.glob("*.json"))

    # Act
    spoiler_logs = load_spoiler_logs(paths)

    # Assert
    assert len(spoiler_logs) == len(paths)
    assert all(isinstance(log, dict) for log in spoiler_logs)


def test_load_spoiler_logs_error_if_not_all_files():
    # Arrange
    paths = [Path("non_existent_file.json")]

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        load_spoiler_logs(paths)


def test_extract_data(resources: Path):
    # Arrange

    # Act
    locations, ages, spawns = extract_data_from_spoiler_logs(
        path=resources, number=2, offset=0
    )

    # Assert
    assert len(locations) == 2
    assert len(ages) == 2
    assert len(spawns) == 2


def test_extract_data_error_if_no_json_files(tmp_path: Path):
    # Arrange

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        extract_data_from_spoiler_logs(path=tmp_path, number=1, offset=0)


def test_extract_data_error_if_offset_out_of_range(resources: Path):
    # Arrange
    paths = list(resources.glob("*.json"))

    # Act / Assert
    with pytest.raises(ValueError):
        extract_data_from_spoiler_logs(path=resources, number=1, offset=len(paths))


def test_extract_data_error_if_offset_negative(resources: Path):
    # Arrange

    # Act / Assert
    with pytest.raises(ValueError):
        extract_data_from_spoiler_logs(path=resources, number=1, offset=-1)
