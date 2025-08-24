from pathlib import Path
import numpy as np
import pandas as pd
import os
from tqdm import tqdm


from data_types import Mode
from src.logic.utils import (
    get_logic,
)
from mylog import logger, setup_csv_logger

import tensorflow as tf


from src.ai.dqn_solver import DQNSolver
from src.ai.environment import OotrEnv

ABS_PATH = os.path.abspath(".")
REP = 1


def run(
    dataset: list[dict[str, str]],
    starting_ages: list[int],
    spawns: list[tuple[str, str]],
    model_path: Path,
    mode: Mode,
):
    with tf.device("/GPU:0"):
        env = OotrEnv()
        observation_space = env.observation_space.shape[0]
        action_space = env.action_space.n
        dqn_solver = DQNSolver(observation_space, action_space, model_path, mode)

        run = 0
        sums_of_rewards = []

        # Output path
        results_path = "results"
        output_path = os.path.join(results_path, "playthroughs")
        if not os.path.isdir(results_path):
            os.mkdir(results_path)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        for f in os.listdir(os.path.join(ABS_PATH, output_path)):
            os.remove(os.path.join(ABS_PATH, output_path, f))

        for rep in range(REP):
            for locations, age, spawn, no_log in tqdm(
                zip(dataset, starting_ages, spawns, no_logs)
            ):
                playthrough = os.path.join(
                    ABS_PATH, f"results/playthroughs/playthrough_{no_log}_{rep}.csv"
                )
                setup_csv_logger(f"playthrough_{no_log}_{rep}", playthrough)
                sum_of_rewards = 0
                dqn_solver.step = 0
                run += 1
                logger.info(f"Seed number {run} | spoiler log no {no_log}")
                state = env.reset(locations, age, spawn)
                state = np.reshape(state, [1, observation_space])
                while True:
                    # env.render()
                    action = dqn_solver.act(state, env, env.already_done(), rep)
                    if action < 0:
                        logger.error("Invalid action, end of episode")
                        break
                    state_next, reward, terminal, info = env.step(
                        action, f"playthrough_{no_log}_{rep}"
                    )
                    reward = reward if not terminal else 600
                    sum_of_rewards += reward
                    state_next = np.reshape(state_next, [1, observation_space])
                    if dqn_solver.step >= 700:
                        reward = -500
                        dqn_solver.remember(
                            state,
                            action,
                            reward,
                            state_next,
                            terminal,
                            env.already_done(),
                            env.state,
                        )
                        logger.warning("Too many steps, end of episode")
                        break
                    dqn_solver.remember(
                        state,
                        action,
                        reward,
                        state_next,
                        terminal,
                        env.already_done(),
                        env.state,
                    )
                    state = state_next
                    if terminal:
                        logger.info(
                            f"Run: {run}, score: {sum_of_rewards}, steps: {dqn_solver.step}"
                        )
                        break
                    if mode == Mode.TRAIN.value:  # no learning when testing
                        dqn_solver.experience_replay()
                if mode == Mode.TRAIN.value:
                    q_values = pd.DataFrame(
                        np.array(dqn_solver.q_value_evolution),
                        columns=list(get_logic().keys())
                        + list(env.additional_actions.keys()),
                    )
                    q_values.to_csv(
                        os.path.join(ABS_PATH, "results/q_values_log.csv"), header=True
                    )
                sums_of_rewards.append(sum_of_rewards)
        dqn_solver.save_model()
        return sums_of_rewards
