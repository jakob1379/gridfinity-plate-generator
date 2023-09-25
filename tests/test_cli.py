"""Test cases for the __main__ module."""
import pytest
from typer.testing import CliRunner

from gridfinity_plate_generator.__main__ import app


@pytest.fixture  # type: ignore
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_cli(runner: CliRunner) -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
