"""
Script to train a reinforcement learning model on Ocarina of Time randomizer
spoiler logs in order to find the shortest path to take to complete the game.
"""

import logging

import matplotlib.pyplot as plt
from src.files_management import extract_logs
from src.ai import train

PATH = 'D:/OoTR_dataset/'
path_bis = 'D:/Weekly_de_m/'

def main():
    # Fetch data
    dataset, ages, spawns, no_logs = extract_logs(path=PATH, n=20)
    #n=11
    #dataset, ages, spawns, no_logs = [dataset[n]], [ages[n]], [spawns[n]], [no_logs[n]]
    sums_of_rewards = train(dataset, ages, spawns, no_logs)
    plot(sums_of_rewards)
    
def plot(scores):
    plt.figure(figsize=(15, 7))
    plt.plot(range(len(scores)), [-s for s in scores])
    plt.xlabel('Number of episodes', size=18)
    plt.ylabel('Time [s]', size=18)
    plt.title('Training scores per episode', size=18)
    plt.savefig('results/training_scores.png')
    

if __name__ == '__main__':
    try:
        main()
        logging.shutdown()
    except:
        logging.shutdown()