"""
Script that handle the ai part of the project.
"""

import numpy as np
import pandas as pd
import math
import logging
import os
from tqdm import tqdm

from gym import spaces
from gym.utils import seeding

from src.logic import get_logic, bool_logic, get_additionnal_actions, get_additionnal_logic
from src.state import State
from src.pathfinder import PathFinder, locations_to_zones
from src.bonus_malus import compute_bonus, compute_malus
from mylog import logger, setup_csv_logger

from collections import deque
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam
import tensorflow as tf
import random


ABS_PATH = os.path.abspath('.')
REP = 1
NO_EXPLORATION = 10000


# useful: https://gsurma.medium.com/cartpole-introduction-to-reinforcement-learning-ed0eb5b58288
class OotrEnv:
    """
    OoTR Environment
    The goal is to create the required environment for a OoTR optimal path 
    solver.
    
    """
    
    def __init__(self):
        self.nb_checks = len(get_logic())
        self.state = State()
        self.junk = -1
        self.major_item = 10
        self.additional_actions = get_additionnal_actions()
        self.action_space = spaces.Discrete(self.nb_checks+len(self.additional_actions))
        self.observation_space = spaces.Box(low=self.calculate_state_observation(blank=True), 
                                            high=self.calculate_state_observation(blank=True, upper_bound=True),
                                            dtype=int)
        
        self.locations = None
        self.observation = None
        self.nb_actions = 0
        self.checks_done = []
        
        self.last_action = []
        self.pathfinder = None
        
        self.trade_items = ['Prescription', 'Eyeball Frog', 'Eyedrops', 'Claim Check']
        self.seed()
    
    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
    
    
    def step(self, action, logger_name):
        bonus = 0
        log = logging.getLogger(logger_name)
        self.nb_actions += 1

        if action >= len(get_logic()):
            action = tuple(self.additional_actions.keys())[action-len(get_logic())]
        else:
            action = tuple(get_logic().keys())[action]
        
        self.last_action.append(action)
        
        #Calculate path
        reward, path = self.pathfinder.from_to(self.state.where, self.pathfinder.convert_to_region(action), self.state)
        
        # Calculate malus
        malus = compute_malus(self.state, action)
        
        if action in get_logic().keys():
            if action == 'Market 10 Big Poes':  # special case
                self.state.item_update('Bottle')
            
            if self.nb_actions % 3 == 0:  # TODO: better implementation
                self.state.item_update('Gold Skulltula Token')
                
            found_item = self.locations[action]
            if isinstance(found_item, dict):  # When bought items
                found_item = found_item['item']
            
            if 'Big Poe' in found_item:
                found_item = 'Big Poe'
            if 'Bottle' in found_item:
                found_item = 'Bottle'
            
            bonus = compute_bonus(self.state, found_item)
            if found_item in self.state.items:
                self.state.item_update(found_item)

            elif found_item in self.trade_items:  # adult trade sequence
                for _ in range(self.trade_items.index(found_item) + 1):
                    self.state.item_update('adult trade sequence')
                    
            
            self.checks_done.append(action)
        else:  # For additionnal actions
            found_item = None
            if isinstance(self.additional_actions[action][-1], list):  #TODO: implement function here
                for effect in self.additional_actions[action][-1]:
                    if '|' in effect:
                        state_change, param = effect.split('|')
                        getattr(self.state, state_change)(param)
                    else:
                        getattr(self.state, effect)()
            else:
                if '|' in self.additional_actions[action][-1]:
                        state_change, param = self.additional_actions[action][-1].split('|')
                        getattr(self.state, state_change)(param)
                else:
                    getattr(self.state, self.additional_actions[action][-1])()

        
        #TODO: incorporate this into a reward_calculating function
        if action == 'Time Travel':
            malus = self.last_action[:-1].count('Time Travel')*4
            if len(self.last_action) >= 2 and self.last_action[-2] == 'Time Travel':
                malus += 50
        
        if reward == -1:
            logger.error(f'Path not found from {self.state.where} to {action}')

        self.state.where = self.pathfinder.convert_to_region(action)
        self.observation = self.calculate_state_observation()
        done = self.state.can_beat_ganon()
        
        if done:
            log.info('GO MODE')
        
        log.info(f"{self.nb_actions},{action},{found_item},{reward},{bonus},{malus},{' -> '.join(path)}")

        # Update reward with bonus and malus
        reward = -reward + bonus - malus
            
        return self.observation, reward, done, (action, found_item)

    def initialise_from_log(self, age, spawn):
        """
        Initialises state according to spoiler log.
        """
        self.state.where = PathFinder.convert_spawn_to_region(spawn[age])
        self.state.set_age(age)
        self.state.set_child_spawn(PathFinder.convert_spawn_to_region(spawn[0]))
        self.state.set_adult_spawn(PathFinder.convert_spawn_to_region(spawn[1]))
        
        # starting song
        loc = ["Song from Saria", "Sheik in Forest", "Song from Ocarina of Time", 
        "Sheik at Colossus", "Sheik at Temple", "Sheik in Kakariko", "Song from Windmill", 
        "Song from Composers Grave", "Sheik in Crater", "Song from Malon", "Sheik in Ice Cavern"]
        songs = ['Minuet of Forest','Bolero of Fire', 'Serenade of Water', 'Requiem of Spirit','Nocturne of Shadow',
                 'Prelude of Light', 'Zeldas Lullaby','Eponas Song','Sarias Song','Suns Song','Song of Time','Song of Storms']
        
        songs_in_log = [self.locations[l] for l in loc if self.locations[l] in songs]
        start_song = list(set(songs)-set(songs_in_log))
        self.state.item_update(start_song[0])
    
    def calculate_state_observation(self, blank=False, upper_bound=False):
        """
        Computes the state input array for the NN.
        """
        state = [x['current'] for x in self.state.items.values()]
        regions = list(locations_to_zones.keys())
        binary_width = np.ceil(np.log2(len(regions))).astype(int)
        
        if blank:
            where = np.binary_repr(len(regions), binary_width) if upper_bound else np.binary_repr(0, binary_width)
        else:

            where = np.binary_repr(regions.index(self.state.where), binary_width)
        state.extend([int(s) for s in where])
        return np.array(state)

    def reset(self, locations, age, spawn):
        self.state = State()
        self.checks_done= []
        self.nb_actions = 0
        self.locations = locations
        self.initialise_from_log(age, spawn)
        self.state.set_initial_ms(locations)
        self.observation = self.calculate_state_observation()
        self.checks_done.append('Links Pocket')
        self.pathfinder = PathFinder(self.state)
        self.last_action = []
        return self.observation
    
    def already_done(self):
        return [1 if x in self.checks_done else 0 for x in get_logic().keys()]


GAMMA = 0.95
LEARNING_RATE = 0.001

MEMORY_SIZE = 1000000
BATCH_SIZE = 20
MEMORY_INTERVAL = 20

EXPLORATION_MAX = 0.15


class DQNSolver:
    def __init__(self, observation_space, action_space, model_path, mode):
        if mode == 'train':
            self.exploration_rate = EXPLORATION_MAX
        else:
            self.exploration_rate = 0

        self.action_space = action_space
        self.memory = deque(maxlen=MEMORY_SIZE)
        
        self.q_value_evolution = []

        self.model_path = model_path
        self.model = self.init_model(observation_space, action_space, model_path)
        
        self.get_stuck = False
        self.step = 0

    def remember(self, state, action, reward, next_state, done, checks_done, next_state_raw):
        self.memory.append((state, action, reward, next_state, done, checks_done, next_state_raw))

    def save_model(self):
        """
        Saves the model at the end of the training.
        """
        self.model.save(self.model_path)
        logger.info(f'Model saved under {self.model_path}')

    @staticmethod
    def init_model(input_size, output_size, path):
        """
        Creates or loads a keras neural network model for deep Q learning.

        input_size(int): size of the input layer
        output_size(int): size of the output layer
        path(string): where to find the model to load.
        """
        def create_model(input_size, output_size):
            m = Sequential()
            m.add(Dense(128, input_shape=(input_size,), activation="relu"))
            m.add(Dense(256, activation="relu"))
            m.add(Dense(output_size, activation="linear"))
            m.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))
            return m

        try:
            model = load_model(path)
            logger.info('Loaded model NN.h5')
        except:
            logger.warning('Could not load model NN.h5, creating a new model instead')
            model = create_model(input_size, output_size)
        return model

    @staticmethod
    def compute_possible_action(state, done_checks):
        """
        Returns a truth array for possible and impossible actions
        
        env(OoTREnv): environment in which the player evolves.
        """
        available_checks = np.concatenate((np.array(bool_logic(state)), np.array(get_additionnal_logic(state), dtype=int)), axis=0)
        mask = np.concatenate((np.array([not x for x in done_checks], dtype=int), np.full(len(get_additionnal_actions()), 1)), axis=0)
        possible_actions = available_checks*mask
        return possible_actions
    
    def q_value_correction(self, state, done_checks):
        """
        Corrections over possible actions to be added to q_values before max or
        argmax.
        
        env(OoTREnv): environment in which the player evolves.
        """
        possible_actions = self.compute_possible_action(state, done_checks)
        return [-math.inf if not x else 0 for x in possible_actions.astype(bool)]

    def act(self, state_rl, env, already_done, exploration_ind):
        """
        
        state_rl: list of number corresponding to state
        state_raw: dict state of player
        """
        self.step += 1
        
        possible_actions = self.compute_possible_action(env.state, env.already_done())
        if sum(possible_actions) == 1:
            if self.get_stuck:
                logger.error('No more checks available ...')
                logger.info(env.state.current_med_name())
                return -1
            self.get_stuck = True
        else:
            self.get_stuck = False
        if exploration_ind % NO_EXPLORATION != 0:  # every NO_EXPLORATION episode, we don't explore
            if np.random.rand() < self.exploration_rate:
                checks_proba = possible_actions
                checks_proba = checks_proba / np.sum(checks_proba)  # Uniform distribution for available checks
                return np.random.choice(np.arange(0, len(checks_proba)), size=1, p=checks_proba)[0]
        q_values = self.model.predict(state_rl)
        q_values = q_values + self.q_value_correction(env.state, env.already_done())
        return np.argmax(q_values[0])

    def experience_replay(self):
        if len(self.memory) < BATCH_SIZE:  # Warmup
            return
        
        if self.step % MEMORY_INTERVAL == 0:
            batch = random.sample(self.memory, BATCH_SIZE)
            for state, action, reward, state_next, terminal, checks_done, state_next_raw in batch:
                q_update = reward
                if not terminal:
                    q_update = reward + GAMMA * np.amax(self.model.predict(state_next)[0]+self.q_value_correction(state_next_raw, checks_done))
                q_values = self.model.predict(state)
                q_values[0][action] = q_update - GAMMA * q_values[0][action]
                self.q_value_evolution.append(q_values[0])
                self.model.fit(state, q_values, verbose=0)
        
        
def run(dataset, starting_ages, spawns, no_logs, model_path, mode='train'):
    with tf.device('/GPU:0'):
        assert mode in ['test', 'train']
        env = OotrEnv()
        observation_space = env.observation_space   .shape[0]
        action_space = env.action_space.n
        dqn_solver = DQNSolver(observation_space, action_space, model_path, mode)

        run = 0
        sums_of_rewards = []

        # Output path
        results_path = 'results'
        output_path = os.path.join(results_path, 'playthroughs')
        if not os.path.isdir(results_path):
            os.mkdir(results_path)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        for f in os.listdir(os.path.join(ABS_PATH, output_path)):
            os.remove(os.path.join(ABS_PATH, output_path, f))

        for rep in range(REP):
            for locations, age, spawn, no_log in tqdm(zip(dataset, starting_ages, spawns, no_logs)):
                playthrough = os.path.join(ABS_PATH, f'results/playthroughs/playthrough_{no_log}_{rep}.csv')
                setup_csv_logger(f'playthrough_{no_log}_{rep}', playthrough)
                sum_of_rewards = 0
                dqn_solver.step = 0
                run += 1
                logger.info(f'Seed number {run} | spoiler log no {no_log}')
                state = env.reset(locations, age, spawn)
                state = np.reshape(state, [1, observation_space])
                while True:
                    # env.render()
                    action = dqn_solver.act(state, env, env.already_done(), rep)
                    if action < 0:
                        logger.error('Invalid action, end of episode')
                        break
                    state_next, reward, terminal, info = env.step(action, f'playthrough_{no_log}_{rep}')
                    reward = reward if not terminal else 600
                    sum_of_rewards += reward
                    state_next = np.reshape(state_next, [1, observation_space])
                    if dqn_solver.step >= 700:
                        reward = -500
                        dqn_solver.remember(state, action, reward, state_next, terminal, env.already_done(), env.state)
                        logger.warning('Too many steps, end of episode')
                        break
                    dqn_solver.remember(state, action, reward, state_next, terminal, env.already_done(), env.state)
                    state = state_next
                    if terminal:
                        logger.info(f"Run: {run}, score: {sum_of_rewards}, steps: {dqn_solver.step}")
                        break
                    if mode == 'train':  # no learning when testing
                        dqn_solver.experience_replay()
                if mode == 'train':
                    q_values = pd.DataFrame(np.array(dqn_solver.q_value_evolution), columns=list(get_logic().keys())+list(env.additional_actions.keys()))
                    q_values.to_csv(os.path.join(ABS_PATH, 'results/q_values_log.csv'), header=True)
                sums_of_rewards.append(sum_of_rewards)
        dqn_solver.save_model()
        return sums_of_rewards
