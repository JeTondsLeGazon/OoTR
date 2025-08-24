import numpy as np
import math


from src.logic.utils import (
    bool_logic,
    get_additionnal_actions,
    get_additionnal_logic,
)
from mylog import logger

from collections import deque
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam
import random
from .config import DeepQNetworkSettings


# useful: https://gsurma.medium.com/cartpole-introduction-to-reinforcement-learning-ed0eb5b58288


settings = DeepQNetworkSettings()


class DQNSolver:
    def __init__(self, observation_space, action_space, model_path, mode):
        if mode == "train":
            self.exploration_rate = settings.exploration_rate
        else:
            self.exploration_rate = 0

        self.action_space = action_space
        self.memory = deque(maxlen=settings.memory_size)

        self.q_value_evolution = []

        self.model_path = model_path
        self.model = self.init_model(observation_space, action_space, model_path)

        self.get_stuck = False
        self.step = 0

    def remember(
        self, state, action, reward, next_state, done, checks_done, next_state_raw
    ):
        self.memory.append(
            (state, action, reward, next_state, done, checks_done, next_state_raw)
        )

    def save_model(self):
        """
        Saves the model at the end of the training.
        """
        self.model.save(self.model_path)
        logger.info(f"Model saved under {self.model_path}")

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
            m.compile(loss="mse", optimizer=Adam(lr=settings.learning_rate))
            return m

        try:
            model = load_model(path)
            logger.info("Loaded model NN.h5")
        except:
            logger.warning("Could not load model NN.h5, creating a new model instead")
            model = create_model(input_size, output_size)
        return model

    @staticmethod
    def compute_possible_action(state, done_checks):
        """
        Returns a truth array for possible and impossible actions

        env(OoTREnv): environment in which the player evolves.
        """
        available_checks = np.concatenate(
            (
                np.array(bool_logic(state)),
                np.array(get_additionnal_logic(state), dtype=int),
            ),
            axis=0,
        )
        mask = np.concatenate(
            (
                np.array([not x for x in done_checks], dtype=int),
                np.full(len(get_additionnal_actions()), 1),
            ),
            axis=0,
        )
        possible_actions = available_checks * mask
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
                logger.error("No more checks available ...")
                logger.info(env.state.current_med_name())
                return -1
            self.get_stuck = True
        else:
            self.get_stuck = False
        if (
            exploration_ind % settings.no_exploration_after_n_steps != 0
        ):  # every NO_EXPLORATION episode, we don't explore
            if np.random.rand() < self.exploration_rate:
                checks_proba = possible_actions
                checks_proba = checks_proba / np.sum(
                    checks_proba
                )  # Uniform distribution for available checks
                return np.random.choice(
                    np.arange(0, len(checks_proba)), size=1, p=checks_proba
                )[0]
        q_values = self.model.predict(state_rl)
        q_values = q_values + self.q_value_correction(env.state, env.already_done())
        return np.argmax(q_values[0])

    def experience_replay(self):
        if len(self.memory) < settings.batch_size:  # Warmup
            return

        if self.step % settings.memory_interval == 0:
            batch = random.sample(self.memory, settings.batch_size)
            for (
                state,
                action,
                reward,
                state_next,
                terminal,
                checks_done,
                state_next_raw,
            ) in batch:
                q_update = reward
                if not terminal:
                    q_update = reward + settings.gamma * np.amax(
                        self.model.predict(state_next)[0]
                        + self.q_value_correction(state_next_raw, checks_done)
                    )
                q_values = self.model.predict(state)
                q_values[0][action] = q_update - settings.gamma * q_values[0][action]
                self.q_value_evolution.append(q_values[0])
                self.model.fit(state, q_values, verbose=0)
