# TODO: use more region for access (DMC, DMT, Graveyard pad)
# TODO: castle grounds may be both adult and child !!!

from src.logic.utils import Requirement, requirements_in_logic
import json

from src.state import State


with open("resources/spawns.json", "r") as f:
    spawns = json.load(f)

with open("resources/zones_to_zones.json", "r") as f:
    zones_to_zones_table = json.load(f)

with open("resources/zone_to_locations.json", "r") as f:
    zones_to_locations_table = json.load(f)


class PathFinder:
    """
    Pathfinder to estimate time necessary to move from one zone to another, depending on the player's state.
    """

    def __init__(self, state: State):
        self.locations_table = zones_to_zones_table.copy()
        self.locations_to_zones = zones_to_locations_table
        self.locations_table.extend(self.get_savewarp(state))
        # TODO: what is this?
        if (
            "anywhere",
            "Colossus",
            5,
            [("Requiem of Spirit", 1)],
        ) in self.locations_table:
            raise ValueError("Weird location")
        self.locations_table.extend(self.get_songwarps())

    def get_region_from_location(self, location: str) -> str:
        for region, locations in self.locations_to_zones.items():
            if location in locations:
                return region
        raise RuntimeError(f"No region found for place {location}")

    @staticmethod
    def get_region_from_spawn(location: str, age: int = 0) -> str:
        if location not in spawns:
            raise ValueError(f"Spawn {location} not found in spawns.json")

        region = spawns.get(location)
        if isinstance(region, dict):
            if age not in region:
                raise ValueError(f"Age {age} not found for spawn {location}")
            return region[age]

        return region

    def get_savewarp(
        self, state: State
    ) -> list[tuple[str, str, int, list[tuple[str, int]]]]:
        """
        Returns an array input from anywhere to the savewarp zone.
        """
        # TODO: change this

        return [
            ("anywhere", state.child_spawn_location, 10, [[{"isadult": False}]]),
            ("anywhere", state.adult_spawn_location, 10, [[{"isadult": True}]]),
        ]

    def get_songwarps(self):
        # TODO: FIX TEST BY CHANGING THIS
        return [
            ("anywhere", "SFM", 5, [("Minuet of Forest", 1)]),
            ("anywhere", "DMC Lower", 5, [("Bolero of Fire", 1)]),
            ("anywhere", "Colossus", 5, [("Requiem of Spirit", 1)]),
            ("anywhere", "Graveyard", 5, [("Nocturne of Shadow", 1)]),
            ("anywhere", "LH", 5, [("Serenade of Water", 1)]),
            ("anywhere", "Temple of Time", 5, [("Prelude of Light", 1)]),
        ]

    # TODO: maybe map locations to enum?
    def from_to(self, from_location: str, to_location: str, state: State):
        """
        Returns the smallest time necessary from a location A to a location B, given the current player's state.
        """
        paths = []
        new_paths = [[[from_location], 0]]
        while True:
            paths = new_paths.copy()
            new_paths.clear()
            for path, t_tot in paths:
                if len(path) > 12:
                    continue
                if path[-1] == to_location:
                    new_paths.append([path, t_tot])
                    if t_tot == min([t for _, t in paths]):
                        return [t_tot, path]
                    continue

                nexts = []
                for first, second, time, requirements_list in self.locations_table:
                    requirements_are_in_logic = any(
                        requirements_in_logic(
                            state,
                            [Requirement.from_dict(r) for r in requirements],
                        )
                        for requirements in requirements_list
                    )

                    if (
                        (path[-1] == first or (first == "anywhere" and len(path) == 1))
                        and second not in path
                        and second != "anywhere"
                        and requirements_are_in_logic
                    ):
                        nexts.append((second, time))

                    if (
                        (
                            path[-1] == second
                            or (second == "anywhere" and len(path) == 1)
                        )
                        and first not in path
                        and first != "anywhere"
                        and requirements_are_in_logic
                    ):
                        nexts.append((first, time))

                for n, t in nexts:
                    new_path = path.copy()
                    new_path.append(n)
                    new_paths.append([new_path, t_tot + t])
            if all(
                [p_[-1] == to_location for p_, _ in new_paths]
            ):  # termination if all paths end in b
                break
        return (
            min([[t, p] for p, t in new_paths]) if len(new_paths) != 0 else [-1, []]
        )  # return minimum time
