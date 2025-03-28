import os
import sys

if os.getenv("flask_inputfilter_dev") or sys.version_info == (3, 14):
    import pyximport

    pyximport.install()

from .InputFilter import InputFilter
