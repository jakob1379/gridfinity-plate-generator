import tempfile

import numpy as np
import plotly.graph_objects as go
import stl
import streamlit as st

from . import gridfinity_generator

version = "0.1.0"
SUPPORT_MAIL = "jakob1379@gmail.com"

if "figs" not in st.session_state:
    st.session_state.figs = {}

st.markdown(
    f"""
<footer style="position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; color: gray; text-align: center;">
<p> ✨ Made by JGA ✨ | Running version {version} | For bug reports 🪲, questions ❓, or feedback 💭, please <a href="https://github.com/jakob1379/gridfinity-plate-generator/issues/">create an issue</a>.</p>
</footer>
""",
    unsafe_allow_html=True,
)


def create_stl_figure(file_name: str) -> go.Figure:
    """Create a 3D figure from an STL file.

    Args:
    - file_name (str): The path to the STL file.

    Returns:
    - go.Figure: A Plotly 3D mesh figure representing the STL.
    """
    mesh = stl.mesh.Mesh.from_file(file_name)

    reshaped_vectors = mesh.vectors.reshape(-1, 3)
    x, y, z = reshaped_vectors.T

    i, j, k = (
        np.arange(0, len(reshaped_vectors), 3),
        np.arange(1, len(reshaped_vectors), 3),
        np.arange(2, len(reshaped_vectors), 3),
    )

    fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, opacity=0.5, cauto=True)])
    fig.update_layout(scene=dict(aspectmode="data"))

    return fig


def generate_and_process(filename_prefix: str, cols: int, rows: int) -> dict:
    """Generate and process the STL files.

    Args:
    - filename_prefix (str): The prefix for the filename.
    - cols (int): Number of columns.
    - rows (int): Number of rows.

    Returns:
    - dict: A dictionary containing figure, path, and name.
    """
    with tempfile.NamedTemporaryFile() as tmpfile:
        filename = f"{tmpfile.name}_{filename_prefix}.stl"
        getattr(gridfinity_generator, filename_prefix)(
            columns=cols, rows=rows, output_filename=filename
        )
        figure = create_stl_figure(filename)
        name = f"gridfinity_{filename_prefix}_{cols}_{rows}_{filename_prefix}.stl".split("/")[-1]

    return {"figure": figure, "path": filename, "name": name}


@st.cache_data(max_entries=10, ttl=180)
def process_user_input(cols: int, rows: int, /) -> dict:
    """Process user input to generate figures and return them.

    Args:
    - cols (int): Number of columns.
    - rows (int): Number of rows.
    Returns:
    - dict: A dictionary containing figures.
    """

    figs = {}
    figs["bottom"] = generate_and_process("bottom", cols, rows)
    figs["base"] = generate_and_process("base", cols, rows)

    return figs


def main():
    """Main function to run the Streamlit app."""
    st.title("Gridfinity Button and Base Generator")
    st.markdown(
        "Welcome! This tool allows you to create any sized gridfinity base plates or buttons, which you can use to attach to your designs for them to fit into the gridfinity universe. Simply choose the number of rows and columns and download your print-ready STL files!"
    )

    st.subheader("Parameters")
    st.write("Here you can set the number of rows and columns")
    with st.form("number_select_form"):
        rows = st.select_slider("rows", options=range(1, 51))
        cols = st.select_slider("columns", options=range(1, 51))
        if st.form_submit_button("Generate!"):
            # Only generate figures if they aren't in the session state or if rows/cols have changed
            if "fig_rows" not in st.session_state or "fig_cols" not in st.session_state:
                st.session_state.figs = process_user_input(*sorted([rows, cols]))

    st.subheader("Preview")
    if st.session_state.figs:
        for plate, col in zip(["bottom", "base"], st.columns(2)):
            col.plotly_chart(st.session_state.figs[plate]["figure"], use_container_width=True)
            with open(st.session_state.figs[plate]["path"], "rb") as f:
                col.download_button(
                    label=f"Download {plate} plate",
                    data=f,
                    mime="model/stl",
                    file_name=st.session_state.figs[plate]["name"],
                )
    else:
        st.write("Use the panel to the left to specify a grid size and preview here!")


if __name__ == "__main__":
    main()
