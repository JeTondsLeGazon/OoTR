import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def resources() -> Path:
    return Path(__file__).parent / "resources"
