import tempfile

import numpy as np
import plotly.graph_objects as go
import stl
import streamlit as st

from gridfinity_plate_generator import gridfinity_generator

version = "0.1.0"
SUPPORT_MAIL = "jakob1379@gmail.com"
params = {}

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

def generate_and_process(
        filename_prefix: str,
        cols: int | None = None,
        rows: int | None = None,
        width: float | None = None,
        length: float | None = None) -> dict:
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

        if cols and rows:
            getattr(gridfinity_generator, filename_prefix)(
                columns=cols, rows=rows, output_filename=filename
            )
        elif width and length:
            getattr(gridfinity_generator, filename_prefix)(
                width=width, length=length, output_filename=filename
            )

    # with tempfile.NamedTemporaryFile() as tmpfile:
    #     filename = f"{tmpfile.name}_{filename_prefix}.stl"
    #     getattr(gridfinity_generator, filename_prefix)(
    #         columns=cols, rows=rows, output_filename=filename
    #     )
        figure = create_stl_figure(filename)
        name = f"gridfinity_{filename_prefix}_{cols}_{rows}_{filename_prefix}.stl".split("/")[-1]

    return {"figure": figure, "path": filename, "name": name}

@st.cache_data(max_entries=10, ttl=180)
def process_user_input(cols: int | None = None, rows: int | None = None, width: float | None = None, length: float | None = None) -> dict:
    """Process user input to generate figures and return them.

    Args:
    - cols (int, optional): Number of columns.
    - rows (int, optional): Number of rows.
    - width (float, optional): Width in millimeters.
    - length (float, optional): Length in millimeters.

    Returns:
    - dict: A dictionary containing figures.
    """

    figs = {}
    if cols and rows:
        figs["bottom"] = generate_and_process("bottom", cols=cols, rows=rows)
        figs["base"] = generate_and_process("base", cols=cols, rows=rows)
    elif width and length:
        figs["bottom"] = generate_and_process("bottom", width=width, length=length)
        figs["base"] = generate_and_process("base", width=width, length=length)

    return figs

def main():
    """Main function to run the Streamlit app."""
    st.title("Gridfinity Bottom and Base Generator 🌐")
    st.markdown(
        "Welcome! 👋 This tool lets you create custom-sized Gridfinity base plates and bottoms. Integrate them into your own designs and join the Gridfinity universe! 🌌 Simply choose your dimensions below and download your ready-to-print STL files! 🖨️"
    )

    st.subheader("Parameters 🛠️")
    st.write("👇 Use either of the forms below to create your grid! 👇")
    params = {}
    with st.form("cols_rows_select_form"):
        st.subheader("Generate using Columns and Rows 📊")
        st.text("With this form, you can generate your grid by specifying the number of columns 📈 and rows 📉.")
        rows = st.select_slider("Rows 📏", options=range(1, 51))
        cols = st.select_slider("Columns 📏", options=range(1, 51))
        if st.form_submit_button("Generate! 🚀"):
            params = {'cols': cols, 'rows': rows}

    with st.form("width_length_select_form"):
        st.subheader("Generate using Width and Length 📐")
        st.text("With this form, you can generate your grid using the width 📏 and length 📏 in millimeters.")
        width = st.number_input("Width (mm) 📏", min_value=0.1, max_value=1000.0, step=0.1)
        length = st.number_input("Length (mm) 📏", min_value=0.1, max_value=1000.0, step=0.1)
        if st.form_submit_button("Generate! 🚀"):
            params = {'width': width, 'length': length}
    # Only generate figures if they aren't in the session state or if width/length have changed
    if "fig_rows" not in st.session_state or "fig_cols" not in st.session_state:
        if ('cols' in params and 'rows' in params) or ('width' in params and 'length' in params):
            st.session_state.figs = process_user_input(**params)

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
