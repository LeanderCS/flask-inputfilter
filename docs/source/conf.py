project = "flask-inputfilter"
copyright = "2025, Leander Cain Slotosch"
author = "Leander Cain Slotosch"
release = "0.3.1"

extensions = ["sphinx_rtd_theme"]

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
