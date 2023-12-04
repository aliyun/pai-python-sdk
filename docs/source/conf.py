# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import sys
from os.path import dirname

doc_root_dir = dirname(dirname(os.path.abspath(__file__)))
sys.path.insert(0, dirname(doc_root_dir))
pkg_root = dirname(doc_root_dir)

import pai

# -- Project information -----------------------------------------------------

project = "PAI Python SDK"
copyright = "2023, Alibaba Cloud"
author = "Alibaba Cloud"

# The full version, including alpha/beta/rc tags
release = pai.version.VERSION
version = pai.version.VERSION


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx_markdown_builder",
    "myst_nb",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build/*",
    "source/_build/*",
    "build/*",
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"
html_title = "PAI Python SDK"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Extension configuration -------------------------------------------------

autoclass_content = "both"
autodoc_member_order = "bysource"

myst_enable_extensions = [
    "substitution",
]

nb_execution_mode = "off"
