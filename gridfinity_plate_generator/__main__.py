import math

import typer

from gridfinity_plate_generator import gridfinity_generator


app = typer.Typer()


@app.command()  # type: ignore
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
) -> None:
    gridfinity_generator.base(
        columns=columns,
        rows=rows,
        output_filename=output_filename,
        baseplate_width=baseplate_width,
        subtracted_square_width=subtracted_square_width,
        rounded_corner_radius=rounded_corner_radius,
        baseplate_height=baseplate_height,
        bottom_chamfer_height=bottom_chamfer_height,
        straight_wall_height=straight_wall_height,
        verbose=verbose,
    )


@app.command()  # type: ignore
def bottom(
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
) -> None:
    bottom(
        columns=columns,
        rows=rows,
        output_filename=output_filename,
        baseplate_width=baseplate_width,
        subtracted_square_width=subtracted_square_width,
        rounded_corner_radius=rounded_corner_radius,
        baseplate_height=baseplate_height,
        bottom_chamfer_height=bottom_chamfer_height,
        straight_wall_height=straight_wall_height,
        verbose=verbose,
    )


if __name__ == "__main__":
    app()
