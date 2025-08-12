import click
from pathlib import Path
from src.files_management import extract_data_from_logs
from src.ai import run


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
    sums_of_rewards = run(data, ages, spawns, model, "train")


cli.add_command(train)
