"""
Pathfinder to estimate time between two zones, depending on state.
"""
# TODO: use more region for access (DMC, DMT, Graveyard pad)
# TODO: castle grounds may be both adult and child !!!

from src.logic import requirements_in_logic
from mylog import logger
import json

with open("resources/location_tables.json", "r") as f:
    locations_table = json.load(f)

with open("resources/locations_to_zones.json", "r") as f:
    locations_to_zones = json.load(f)

with open("resources/spawns.json", "r") as f:
    spawns = json.load(f)


class PathFinder:
    def __init__(self, state):
        self.locations_table = locations_table.copy()
        self.locations_to_zones = locations_to_zones
        self.locations_table.extend(self.savewarp(state))
        if (
            "anywhere",
            "Colossus",
            5,
            [("Requiem of Spirit", 1)],
        ) in self.locations_table:
            print("Oups")
        self.locations_table.extend(self.songwarp())

    def convert_to_region(self, place):
        for k, v in self.locations_to_zones.items():
            if place in v:
                return k
        logger.error(f"No region found for place {place}")
        return ""

    @staticmethod
    def convert_spawn_to_region(place, age=0):
        try:
            if place == "Castle Grounds":
                return spawns[place][age]
            else:
                return spawns[place]
        except:
            logger.error(f"No spawn found at {place}")
            return ""

    def savewarp(self, state):
        """
        Returns an array input from anywhere to the savewarp zone.
        """

        return [
            ("anywhere", state.child_spawn, 10, [("isadult", 0)]),
            ("anywhere", state.adult_spawn, 10, [("isadult", 1)]),
        ]

    def songwarp(self):
        return [
            ("anywhere", "SFM", 5, [("Minuet of Forest", 1)]),
            ("anywhere", "DMC Lower", 5, [("Bolero of Fire", 1)]),
            ("anywhere", "Colossus", 5, [("Requiem of Spirit", 1)]),
            ("anywhere", "Graveyard", 5, [("Nocturne of Shadow", 1)]),
            ("anywhere", "LH", 5, [("Serenade of Water", 1)]),
            ("anywhere", "Temple of Time", 5, [("Prelude of Light", 1)]),
        ]

    def from_to(self, a, b, state):
        """
        Returns the smallest time necessary from a to b given a state.
        """
        paths = []
        new_paths = [[[a], 0]]
        while True:
            paths = new_paths.copy()
            new_paths.clear()
            for path, t_tot in paths:
                if len(path) > 12:
                    continue
                if path[-1] == b:
                    new_paths.append([path, t_tot])
                    if t_tot == min([t for _, t in paths]):
                        return [t_tot, path]
                    continue

                nexts = []
                for first, second, time, req in self.locations_table:
                    if (
                        (path[-1] == first or (first == "anywhere" and len(path) == 1))
                        and second not in path
                        and second != "anywhere"
                        and self.in_logic(state, req, path[-1])
                    ):
                        nexts.append((second, time))

                    if (
                        (
                            path[-1] == second
                            or (second == "anywhere" and len(path) == 1)
                        )
                        and first not in path
                        and first != "anywhere"
                        and self.in_logic(state, req, path[-1])
                    ):
                        nexts.append((first, time))

                for n, t in nexts:
                    new_path = path.copy()
                    new_path.append(n)
                    new_paths.append([new_path, t_tot + t])
            if all(
                [p_[-1] == b for p_, _ in new_paths]
            ):  # termination if all paths end in b
                break
        return (
            min([[t, p] for p, t in new_paths]) if len(new_paths) != 0 else [-1, []]
        )  # return minimum time

    def in_logic(self, state, req, where):
        if len(req) == 0:
            return True

        elif isinstance(req[0], tuple):  # Only one logic possible
            return requirements_in_logic(state, req, where)

        else:  # Many logics possible
            return any([requirements_in_logic(state, rr, where) for rr in req])
