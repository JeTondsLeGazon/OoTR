import click
import matplotlib.pyplot as plt
from pathlib import Path
from src.spoiler_logs.utils import extract_data_from_logs
from src.ai import run
from src.data_types import Mode


@click.group()
def cli():
    "CLI entrypoint"
    pass


@click.command()
@click.option(
    "--dataset",
    type=Path,
    required=True,
    help="Path to repository containing spoiler logs",
)
@click.option(
    "--number",
    "-n",
    type=int,
    required=False,
    default=1000,
    help="Number of logs to process",
)
@click.option(
    "--offset",
    type=int,
    required=False,
    default=0,
    help="Offset for the logs to process",
)
@click.option(
    "--model",
    type=Path,
    required=False,
    default="NN.h5",
    help="Path to the trained neural network model file to output",
)
def train(dataset: Path, number: int, offset: int, model: Path) -> None:
    # TODO: enable continue training
    data, ages, spawns = extract_data_from_logs(
        path=dataset, number=number, offset=offset
    )
    sums_of_rewards = run(data, ages, spawns, model, Mode.TRAIN)
    plot(sums_of_rewards)


def plot(scores):
    plt.figure(figsize=(15, 7))
    plt.plot(range(len(scores)), [-s for s in scores])
    plt.xlabel("Number of episodes", size=18)
    plt.ylabel("Time [s]", size=18)
    plt.title("Training scores per episode", size=18)
    plt.savefig("results/training_scores.png")


cli.add_command(train)
