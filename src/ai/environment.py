import numpy as np
import logging

# TODO: update to gymnsasium to support numpy 2.* or pin versions
from gym import spaces
from gym.utils import seeding

from src.logic.utils import (
    get_logic,
    get_additionnal_actions,
)
from src.state import State
from src.pathfinder import PathFinder, locations_to_zones
from src.bonus_malus import compute_bonus, compute_malus
from mylog import logger


class OotrEnv:
    """
    OoTR Environment
    Represents the environement for the Deep learning training.

    """

    def __init__(self):
        self.nb_checks = len(get_logic())
        self.state = State()
        self.junk = -1
        self.major_item = 10
        self.additional_actions = get_additionnal_actions()
        self.action_space = spaces.Discrete(
            self.nb_checks + len(self.additional_actions)
        )
        self.observation_space = spaces.Box(
            low=self.calculate_state_observation(blank=True),
            high=self.calculate_state_observation(blank=True, upper_bound=True),
            dtype=int,
        )

        self.locations = None
        self.observation = None
        self.nb_actions = 0
        self.checks_done = []

        self.last_action = []
        self.pathfinder = None

        self.trade_items = ["Prescription", "Eyeball Frog", "Eyedrops", "Claim Check"]
        self.set_seed()

    def set_seed(self, seed: int | None = None) -> None:
        self.np_random, seed = seeding.np_random(seed)

    def step(self, action, logger_name):
        bonus = 0
        log = logging.getLogger(logger_name)
        self.nb_actions += 1

        if action >= len(get_logic()):
            action = tuple(self.additional_actions.keys())[action - len(get_logic())]
        else:
            action = tuple(get_logic().keys())[action]

        self.last_action.append(action)

        # Calculate path
        reward, path = self.pathfinder.from_to(
            self.state.where,
            self.pathfinder.get_region_from_location(action),
            self.state,
        )

        # Calculate malus
        malus = compute_malus(self.state, action)

        # Skull update
        if self.nb_actions % 9 == 0:  # TODO: better implementation
            self.state.item_update("Gold Skulltula Token")
            self.state.item_update("Gold Skulltula Token")
            self.state.item_update("Gold Skulltula Token")
            self.state.item_update("Gold Skulltula Token")

        if action in get_logic().keys():
            if action == "Market 10 Big Poes":  # special case
                self.state.item_update("Bottle")

            found_item = self.locations[action]
            if isinstance(found_item, dict):  # When bought items
                found_item = found_item["item"]

            if "Big Poe" in found_item:
                found_item = "Big Poe"
            if "Bottle" in found_item:
                found_item = "Bottle"

            bonus = compute_bonus(self.state, found_item)
            if found_item in self.state.items:
                self.state.item_update(found_item)

            elif found_item in self.trade_items:  # adult trade sequence
                for _ in range(self.trade_items.index(found_item) + 1):
                    self.state.item_update("adult trade sequence")

            self.checks_done.append(action)
        else:  # For additionnal actions
            found_item = None
            if isinstance(
                self.additional_actions[action][-1], list
            ):  # TODO: implement function here
                for effect in self.additional_actions[action][-1]:
                    if "|" in effect:
                        state_change, param = effect.split("|")
                        getattr(self.state, state_change)(param)
                    else:
                        getattr(self.state, effect)()
            else:
                if "|" in self.additional_actions[action][-1]:
                    state_change, param = self.additional_actions[action][-1].split("|")
                    getattr(self.state, state_change)(param)
                else:
                    getattr(self.state, self.additional_actions[action][-1])()

        # TODO: incorporate this into a reward_calculating function
        if action == "Time Travel":
            malus = self.last_action[:-1].count("Time Travel") * 4
            if len(self.last_action) >= 2 and self.last_action[-2] == "Time Travel":
                malus += 50

        if reward == -1:
            logger.error(f"Path not found from {self.state.where} to {action}")

        self.state.where = self.pathfinder.get_region_from_location(action)
        self.observation = self.calculate_state_observation()
        done = self.state.can_beat_ganon()

        if done:
            log.info("GO MODE")

        log.info(
            f"{self.nb_actions},{action},{found_item},{reward},{bonus},{malus},{' -> '.join(path)}"
        )

        # Update reward with bonus and malus
        reward = -reward + bonus - malus

        return self.observation, reward, done, (action, found_item)

    def initialise_from_log(self, age: int, spawn: tuple[str, str]):
        """
        Initialises state according to spoiler log.
        """
        self.state.current_location = PathFinder.get_region_from_spawn(spawn[age])
        self.state.set_age(age)
        self.state.child_spawn_location = PathFinder.get_region_from_spawn(spawn[0], 0)
        self.state.adult_spawn_location = PathFinder.get_region_from_spawn(spawn[1], 1)

        # starting song
        locations = [
            "Song from Saria",
            "Sheik in Forest",
            "Song from Ocarina of Time",
            "Sheik at Colossus",
            "Sheik at Temple",
            "Sheik in Kakariko",
            "Song from Windmill",
            "Song from Composers Grave",
            "Sheik in Crater",
            "Song from Malon",
            "Sheik in Ice Cavern",
        ]
        songs = [
            "Minuet of Forest",
            "Bolero of Fire",
            "Serenade of Water",
            "Requiem of Spirit",
            "Nocturne of Shadow",
            "Prelude of Light",
            "Zeldas Lullaby",
            "Eponas Song",
            "Sarias Song",
            "Suns Song",
            "Song of Time",
            "Song of Storms",
        ]

        songs_in_log = [
            self.locations[location]
            for location in locations
            if self.locations[location] in songs
        ]
        start_song = list(set(songs) - set(songs_in_log))
        self.state.item_update(start_song[0])

    def calculate_state_observation(self, blank=False, upper_bound=False):
        """
        Computes the state input array for the NN.
        """
        state = [x["current"] for x in self.state.items.values()]
        regions = list(locations_to_zones.keys())
        binary_width = np.ceil(np.log2(len(regions))).astype(int)

        if blank:
            where = (
                np.binary_repr(len(regions), binary_width)
                if upper_bound
                else np.binary_repr(0, binary_width)
            )
        else:
            where = np.binary_repr(regions.index(self.state.where), binary_width)
        state.extend([int(s) for s in where])
        return np.array(state)

    def reset(self, locations, age, spawn):
        self.state = State()
        self.checks_done = []
        self.nb_actions = 0
        self.locations = locations
        self.initialise_from_log(age, spawn)
        self.state.set_initial_ms(locations)
        self.observation = self.calculate_state_observation()
        self.checks_done.append("Links Pocket")
        self.pathfinder = PathFinder(self.state)
        self.last_action = []
        return self.observation

    def already_done(self):
        return [1 if x in self.checks_done else 0 for x in get_logic().keys()]
