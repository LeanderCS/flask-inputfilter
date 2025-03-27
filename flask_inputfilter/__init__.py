import os

if os.getenv("flask_inputfilter_dev"):
    import pyximport

    pyximport.install()

from .InputFilter import InputFilter
