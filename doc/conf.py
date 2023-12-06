# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Weather Station'
copyright = '2023, Gavrila Andreea-Alexandra, Barbulet Ana-Maria, Cacu Razvan'
author = 'Gavrila Andreea-Alexandra, Barbulet Ana-Maria, Cacu Razvan'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# Specify the main toctree document
master_doc = 'index'

# List of documents to include in the build
html_sidebars = {
    '**': ['globaltoc.html', 'sourcelink.html', 'searchbox.html'],
}
html_theme_options = {
    'style_nav_header_background': '#5eabff',
}

# Specify the main toctree document and other documents to include
toctree_documents = [
    'index',
    'forecast_open_weather_example',
    # Add other documents as needed
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'bizstyle'
html_static_path = ['_static']
