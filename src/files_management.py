from typing import Any
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

Log = dict[str, Any]  # Define a type alias for the log dictionary structure


def extract_json(json_files: list[Path]) -> list[Log]:
    """Loads json dict from many json files."""
    extracted_dicts = []
    for json_file in json_files:
        try:
            with json_file.open() as f:
                extracted_dicts.append(json.load(f))
        except Exception as e:
            logger.error(f"Failed to load {json_file}: {e}")
    return extracted_dicts


def extract_locations(spoiler_logs: list[Log]) -> list[dict[str, str]]:
    """Extracts the locations from the spoiler logs dicts."""
    if not all("locations" in log for log in spoiler_logs):
        raise ValueError("Some logs are missing 'locations' key")

    return [log["locations"] for log in spoiler_logs]


def extract_age(spoiler_logs: list[Log]) -> list[int]:
    """Extracts the starting age from the spoiler logs dicts."""
    return [
        0 if log.get("randomized_settings", {}).get("starting_age") == "child" else 1
        for log in spoiler_logs
    ]


def extract_spawn(spoiler_logs: list[Log]) -> list[tuple[str, str]]:
    """Extracts the starting spawns from the spoiler logs dicts."""
    spawns = []
    for log in spoiler_logs:
        child_spawn = log.get("entrances", {}).get("Child Spawn -> KF Links House")
        adult_spawn = log.get("entrances", {}).get("Adult Spawn -> Temple of Time")
        spawns.append(
            (
                child_spawn["region"] if isinstance(child_spawn, dict) else child_spawn,
                adult_spawn["region"] if isinstance(adult_spawn, dict) else adult_spawn,
            )
        )
    return spawns


def extract_data_from_logs(
    path: Path, number: int = 1000, offset: int = 0
) -> tuple[list[dict[str, str]], list[int], list[tuple[str, str]]]:
    """
    Extracts items location from n spoiler log files and returns lists.
    Only processes files in the requested range for efficiency.
    """
    json_files = list(path.glob("*.json"))

    if not json_files:
        raise FileNotFoundError(f"No JSON files found in {path}")

    if offset < 0 or offset >= len(json_files):
        raise ValueError(
            f"Offset {offset} is out of range for the number of files {len(json_files)}"
        )

    if number <= 0 or offset + number > len(json_files):
        raise ValueError(
            f"Number {number} with offset {offset} exceeds the number of available files {len(json_files)}"
        )

    selected_files = json_files[offset : offset + number]
    spoiler_logs = extract_json(selected_files)
    locations = extract_locations(spoiler_logs)
    starting_ages = extract_age(spoiler_logs)
    starting_spawns = extract_spawn(spoiler_logs)
    logger.info(f"Successfully extracted locations from {len(locations)} files")
    return locations, starting_ages, starting_spawns
