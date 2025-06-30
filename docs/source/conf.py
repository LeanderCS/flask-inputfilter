import os
import sys

project = "flask-inputfilter"
copyright = "2025, Leander Cain Slotosch"
author = "Leander Cain Slotosch"

extensions = [
    "sphinx_rtd_theme",
    "sphinx_design",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

autodoc_default_options = {
    "show-inheritance": True,
}

autodoc_member_order = "bysource"
autodoc_typehints = "description"
autoclass_content = "both"

autodoc_type_aliases = {
    "EstimatorPubLike": "EstimatorPubLike",
    "SamplerPubLike": "SamplerPubLike",
}

autosummary_generate = True
autosummary_generate_overwrite = False

napoleon_google_docstring = True
napoleon_numpy_docstring = False

sys.path.insert(0, os.path.abspath("../.."))

templates_path = []
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["style.css"]
html_js_files = [
    (
        "https://www.googletagmanager.com/gtag/js?id=G-778965FXHK",
        {"async": "async"},
    ),
    ("google-analytics.js", {}),
]
html_extra_path = ["_static/google-analytics.js"]
html_theme_options = {"navigation_depth": 4}
html_favicon = "_static/favicon.ico"
