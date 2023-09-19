import math

import typer

from gridfinity_plate_generator import gridfinity_generator

app = typer.Typer()


@app.command()
def base(
    columns: int = typer.Option(3, "--columns", "-c"),
    rows: int = typer.Option(3, "--rows", "-r"),
    output_filename: str = typer.Option(None, "--output", "-o"),
    baseplate_width: float = typer.Option(42, "--baseplate-width"),
    subtracted_square_width: float = typer.Option(42.71, "--subtracted-square-width"),
    rounded_corner_radius: float = typer.Option(4, "--rounded-corner-radius"),
    baseplate_height: float = typer.Option(5, "--baseplate-height"),
    bottom_chamfer_height: float = typer.Option(0.985 / math.sqrt(2), "--bottom-chamfer-height"),
    straight_wall_height: float = typer.Option(1.8, "--straight-wall-height"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    gridfinity_generator.base(
        columns,
        rows,
        output_filename,
        baseplate_width,
        subtracted_square_width,
        rounded_corner_radius,
        baseplate_height,
        bottom_chamfer_height,
        straight_wall_height,
        verbose,
    )


@app.command()
def buttom(
    columns: int = typer.Option(3, "--columns", "-c"),
    rows: int = typer.Option(3, "--rows", "-r"),
    output_filename: str = typer.Option(None, "--output", "-o"),
    baseplate_width: float = typer.Option(42, "--baseplate-width"),
    subtracted_square_width: float = typer.Option(42.71, "--subtracted-square-width"),
    rounded_corner_radius: float = typer.Option(4, "--rounded-corner-radius"),
    baseplate_height: float = typer.Option(5, "--baseplate-height"),
    bottom_chamfer_height: float = typer.Option(0.985 / math.sqrt(2), "--bottom-chamfer-height"),
    straight_wall_height: float = typer.Option(1.8, "--straight-wall-height"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    buttom(
        columns,
        rows,
        output_filename,
        baseplate_width,
        subtracted_square_width,
        rounded_corner_radius,
        baseplate_height,
        bottom_chamfer_height,
        straight_wall_height,
        verbose,
    )


if __name__ == "__main__":
    app()
