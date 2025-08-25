"""User interface to create gridfinity models with gridfinity_plate_generator module."""

import logging
import os
import tempfile
from dataclasses import dataclass
from enum import Enum
from typing import Dict
from typing import Optional
from typing import Tuple

import numpy as np
import plotly.graph_objects as go
import stl
import streamlit as st

from gridfinity_plate_generator import gridfinity_generator


# Constants
VERSION = "0.1.0"
GITHUB_ISSUES_URL = "https://github.com/jakob1379/gridfinity-plate-generator/issues/"
MAX_GRID_SIZE = 50
MAX_DIMENSION_MM = 1000.0

# Configure logging
logging.basicConfig(
    filename="gridfinity.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class PlateType(str, Enum):
    """Types of plates that can be generated."""

    BASE = "base"
    BOTTOM = "bottom"


@dataclass
class GeneratedModel:
    """Container for generated model data."""

    figure: go.Figure
    path: str
    name: str


def setup_page() -> None:
    """Configure page title and footer."""
    st.title("Gridfinity Bottom and Base Generator ")
    st.markdown(
        """Welcome!

        This tool lets you create custom-sized Gridfinity base plates and bottoms.
        Integrate them into your own designs and join the Gridfinity universe! 🌌
        Simply choose your dimensions below and download your ready-to-print STL files! 🖨️
        """
    )

    # Footer
    st.markdown(
        f"""
        <footer style="position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: white; color: gray; text-align: center;">
        <p> ✨ made by jga ✨ | running version {VERSION} |
        for bug reports 🪲, questions ❓, or feedback 💭,
        please <a href="{GITHUB_ISSUES_URL}">create an issue</a>.</p>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def create_stl_figure(file_path: str) -> go.Figure:
    """Create a 3D figure from an STL file.

    Args:
        file_path: Path to the STL file

    Returns:
        A Plotly 3D mesh figure representing the STL
    """
    logger.debug(f"Creating 3D figure from {file_path}")
    mesh = stl.mesh.Mesh.from_file(file_path)

    # Reshape the vectors for plotting
    reshaped_vectors = mesh.vectors.reshape(-1, 3)
    x, y, z = reshaped_vectors.T

    # Create triangular mesh indices
    i = np.arange(0, len(reshaped_vectors), 3)
    j = np.arange(1, len(reshaped_vectors), 3)
    k = np.arange(2, len(reshaped_vectors), 3)

    # Create the 3D mesh figure
    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=x, y=y, z=z, i=i, j=j, k=k, opacity=0.5, cauto=True, colorscale="Viridis"
            )
        ]
    )
    fig.update_layout(
        scene=dict(
            aspectmode="data",
            xaxis_title="X (mm)",
            yaxis_title="Y (mm)",
            zaxis_title="Z (mm)",
        )
    )

    return fig


def generate_model(
    plate_type: PlateType,
    cols: Optional[int] = None,
    rows: Optional[int] = None,
    width: Optional[float] = None,
    length: Optional[float] = None,
) -> GeneratedModel:
    """Generate a gridfinity model and create a 3D visualization.

    Args:
        plate_type: Type of plate to generate (base or bottom)
        cols: Number of columns (grid-based generation)
        rows: Number of rows (grid-based generation)
        width: Width in mm (dimension-based generation)
        length: Length in mm (dimension-based generation)

    Returns:
        Object containing the figure, file path, and filename
    """
    logger.info(
        f"Generating {plate_type} with cols={cols}, rows={rows}, width={width}, length={length}"
    )

    # Create a temporary file that won't be automatically deleted
    fd, filename = tempfile.mkstemp(suffix=".stl")
    os.close(fd)  # Close the file descriptor but keep the file

    generator_func = getattr(gridfinity_generator, plate_type)

    # Call the appropriate generator function with the right parameters
    if cols is not None and rows is not None:
        generator_func(columns=cols, rows=rows, output_filename=filename)
        name = f"gridfinity_{plate_type}_{cols}x{rows}.stl"
    elif width is not None and length is not None:
        generator_func(width=width, length=length, output_filename=filename)
        name = f"gridfinity_{plate_type}_{width}x{length}mm.stl"
    else:
        raise ValueError("Either (cols, rows) or (width, length) must be provided")

    figure = create_stl_figure(filename)

    # Return an object with all the model data
    return GeneratedModel(figure=figure, path=filename, name=name)


def process_user_input(
    cols: Optional[int] = None,
    rows: Optional[int] = None,
    width: Optional[float] = None,
    length: Optional[float] = None,
) -> Dict[PlateType, GeneratedModel]:
    """Process user input to generate figures and return them.

    Args:
        cols: Number of columns (grid-based generation)
        rows: Number of rows (grid-based generation)
        width: Width in mm (dimension-based generation)
        length: Length in mm (dimension-based generation)

    Returns:
        Dictionary mapping plate types to their generated models
    """
    logger.info(f"Processing user input: cols={cols}, rows={rows}, width={width}, length={length}")

    models = {}

    if (cols is not None and rows is not None) or (width is not None and length is not None):
        models[PlateType.BOTTOM] = generate_model(
            PlateType.BOTTOM, cols=cols, rows=rows, width=width, length=length
        )
        models[PlateType.BASE] = generate_model(
            PlateType.BASE, cols=cols, rows=rows, width=width, length=length
        )

    return models


def display_models(models: Dict[PlateType, GeneratedModel]) -> None:
    """Display the generated models with download buttons.

    Args:
        models: Dictionary mapping plate types to their generated models
    """
    st.header("Preview")

    if not models:
        st.info("Use the forms above to generate models. The preview will appear here.")
        return

    # Create columns for side-by-side display
    cols = st.columns(2)

    for idx, plate_type in enumerate([PlateType.BOTTOM, PlateType.BASE]):
        if plate_type not in models:
            continue

        model = models[plate_type]
        col = cols[idx]

        # Display the 3D model
        col.subheader(f"{plate_type.capitalize()}")
        col.plotly_chart(model.figure, use_container_width=True)

        # Add download button
        try:
            with open(model.path, "rb") as f:
                col.download_button(
                    label=f"Download {plate_type.value} plate",
                    data=f,
                    mime="model/stl",
                    file_name=model.name,
                )
        except FileNotFoundError:
            col.error(f"Error: File for {plate_type.value} plate not found. Please regenerate the model.")
            logger.error(f"File not found: {model.path}")


def grid_input_form() -> Tuple[Optional[int], Optional[int]]:
    """Form for grid-based input (columns and rows).

    Returns:
        Tuple of (columns, rows) if form was submitted, otherwise (None, None)
    """
    with st.form("grid_form"):
        st.subheader("Generate using Columns and Rows 📊")
        st.text(
            "Specify the number of columns and rows to generate a grid-based plate."
        )

        cols = st.select_slider("Columns 📏", options=range(1, MAX_GRID_SIZE + 1), value=3)
        rows = st.select_slider("Rows 📏", options=range(1, MAX_GRID_SIZE + 1), value=3)

        submitted = st.form_submit_button("Generate Grid! 🚀")

        return (cols, rows) if submitted else (None, None)


def dimension_input_form() -> Tuple[Optional[float], Optional[float]]:
    """Form for dimension-based input (width and length).

    Returns:
        Tuple of (width, length) if form was submitted, otherwise (None, None)
    """
    with st.form("dimension_form"):
        st.subheader("Generate using Width and Length 📐")
        st.text(
            "Specify the exact dimensions in millimeters to generate a custom-sized plate."
        )

        width = st.number_input(
            "Width (mm) 📏",
            min_value=10.0,
            max_value=MAX_DIMENSION_MM,
            value=84.0,  # Default is 3 grid units (3 * 28mm)
            step=1.0
        )
        length = st.number_input(
            "Length (mm) 📏",
            min_value=10.0,
            max_value=MAX_DIMENSION_MM,
            value=84.0,  # Default is 3 grid units
            step=1.0
        )

        submitted = st.form_submit_button("Generate Custom Size! 🚀")

        return (width, length) if submitted else (None, None)


def main() -> None:
    """Main function to run the Streamlit app."""
    try:
        logger.info("Starting Gridfinity Plate Generator application")

        # Initialize session state if needed
        if "models" not in st.session_state:
            st.session_state.models = {}

        # Setup page UI
        setup_page()

        # Parameter section
        st.subheader("Parameters 🛠️")
        st.write("Use either of the forms below to create your Gridfinity plate!")

        # Input forms
        cols, rows = grid_input_form()
        width, length = dimension_input_form()

        # Create a placeholder for the preview section
        preview_placeholder = st.empty()

        # Process input if any form was submitted
        if cols is not None and rows is not None:
            with preview_placeholder.container():
                st.subheader("Preview")
                with st.spinner("Generating grid plates... This may take a moment ⏳", show_time=True):
                    st.session_state.models = process_user_input(cols=cols, rows=rows)
        elif width is not None and length is not None:
            with preview_placeholder.container():
                st.subheader("Preview")
                with st.spinner("Generating custom plates... This may take a moment ⏳", show_time=True):
                    st.session_state.models = process_user_input(width=width, length=length)

        # Display models
        if cols is not None or width is not None:
            # Clear the spinner and display the models
            preview_placeholder.empty()
            display_models(st.session_state.models)
        else:
            # Just display the models or empty state
            display_models(st.session_state.models)

        # Clean up old temporary files when the app refreshes
        if hasattr(st.session_state, 'previous_models'):
            for plate_type, model in st.session_state.previous_models.items():
                try:
                    if os.path.exists(model.path):
                        os.remove(model.path)
                        logger.debug(f"Cleaned up old file: {model.path}")
                except Exception as e:
                    logger.warning(f"Error cleaning up file {model.path}: {e}")

        # Store current models for cleanup in next run
        st.session_state.previous_models = st.session_state.models

    except Exception as e:
        logger.exception("An error occurred in the main application")
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check the logs or report this issue on GitHub.")


if __name__ == "__main__":
    main()

