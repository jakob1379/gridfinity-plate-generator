"""Sphinx configuration."""
project = "Gridfinity Plate Generator"
author = "Jakob Guldberg Aaes"
copyright = "2023, Jakob Guldberg Aaes"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
