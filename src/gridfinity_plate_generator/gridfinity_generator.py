import logging
import math

import cadquery as cq

import typer

from .config import (
    default_baseplate_height,
    default_baseplate_width,
    default_bottom_chamfer_height,
    default_columns,
    default_output_filename,
    default_rounded_corner_radius,
    default_rows,
    default_straight_wall_height,
    default_subtracted_square_width,
    default_verbose,
)

app = typer.Typer()


def setup_logging(verbose: bool):
    """Set up logging based on the verbose flag."""
    logging.basicConfig(
        format="[%(levelname)s]: %(message)s",
        level=logging.DEBUG if verbose else logging.WARNING,
    )


def create_grid_squares(
    baseplate_height,
    bottom_chamfer_height,
    straight_wall_height,
    subtracted_square_width,
    rounded_corner_radius,
    baseplate_width,
    columns,
    rows,
):
    top_chamfer_height = baseplate_height - bottom_chamfer_height - straight_wall_height

    logging.info("Creating 2D sketch with rounded corners for grid squares...")
    rounded_square = (
        cq.Sketch()
        .rect(subtracted_square_width, subtracted_square_width)
        .vertices()
        .fillet(rounded_corner_radius)
    )

    logging.info("Creating the tool used to subtract grid squares from the baseplate...")
    square_subtraction_tool = (
        cq.Workplane("XY")
        .placeSketch(rounded_square)
        .extrude(top_chamfer_height * math.sqrt(2), taper=45)
        .faces(">Z")
        .wires()
        .toPending()
        .extrude(straight_wall_height)
        .faces(">Z")
        .wires()
        .toPending()
        .extrude(bottom_chamfer_height * math.sqrt(2), taper=45)
        .rotate((0, 0, 0), (1, 0, 0), 180)
        .translate((baseplate_width / 2, baseplate_width / 2, baseplate_height))
    )

    logging.info("Determining grid square positions...")
    grid_square_positions = [
        (x * baseplate_width, y * baseplate_width)
        for x in range(0, columns)
        for y in range(0, rows)
    ]

    logging.info("Combining grid squares for subtraction...")
    combined_grid_squares = (
        cq.Workplane("XY")
        .pushPoints(grid_square_positions)
        .eachpoint(
            lambda loc: square_subtraction_tool.val().moved(loc),
            combine="a",
            clean=True,
        )
    )
    return combined_grid_squares


def base(
    columns: int = default_columns,
    rows: int = default_rows,
    output_filename: str | None = default_output_filename,
    baseplate_width: float = default_baseplate_width,
    subtracted_square_width: float = default_subtracted_square_width,
    rounded_corner_radius: float = default_rounded_corner_radius,
    baseplate_height: float = default_baseplate_height,
    bottom_chamfer_height: float = default_bottom_chamfer_height,
    straight_wall_height: float = default_straight_wall_height,
    verbose: bool = default_verbose,
):
    setup_logging(verbose)

    combined_grid_squares = create_grid_squares(
        baseplate_height,
        bottom_chamfer_height,
        straight_wall_height,
        subtracted_square_width,
        rounded_corner_radius,
        baseplate_width,
        columns,
        rows,
    )

    logging.info("Creating the Gridfinity baseplate and subtracting the grid squares...")
    gridfinity_baseplate = (
        cq.Workplane("XY")
        .box(columns * baseplate_width, rows * baseplate_width, baseplate_height - 0.001)
        .edges("|Z")
        .fillet(rounded_corner_radius)
        .translate(
            (
                columns * baseplate_width / 2,
                rows * baseplate_width / 2,
                baseplate_height / 2,
            )
        )
        .faces(">Z")
        .cut(combined_grid_squares)
    )

    if output_filename is not None:
        logging.info(f"Saving to {output_filename}")
        cq.exporters.export(
            gridfinity_baseplate, output_filename, tolerance=0.99, angularTolerance=0.5
        )

    return gridfinity_baseplate


def bottom(
    columns: int = default_columns,
    rows: int = default_rows,
    output_filename: str | None = default_output_filename,
    baseplate_width: float = default_baseplate_width,
    subtracted_square_width: float = default_subtracted_square_width,
    rounded_corner_radius: float = default_rounded_corner_radius,
    baseplate_height: float = default_baseplate_height,
    bottom_chamfer_height: float = default_bottom_chamfer_height,
    straight_wall_height: float = default_straight_wall_height,
    verbose: bool = default_verbose,
):
    setup_logging(verbose)

    combined_grid_squares = create_grid_squares(
        baseplate_height,
        bottom_chamfer_height,
        straight_wall_height,
        subtracted_square_width,
        rounded_corner_radius,
        baseplate_width,
        columns,
        rows,
    )

    logging.info("Creating the Gridfinity baseplate and subtracting the grid squares...")

    if output_filename is not None:
        logging.info(f"Saving to {output_filename}")
        cq.exporters.export(
            combined_grid_squares, output_filename, tolerance=0.99, angularTolerance=0.5
        )
    return combined_grid_squares


if __name__ == "__main__":
    app()
