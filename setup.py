import os

from Cython.Build import cythonize
from setuptools import setup

os.environ["CC"] = "g++"
os.environ["CXX"] = "g++"

setup(
    ext_modules=cythonize(
        [
            "flask_inputfilter/Mixin/ExternalApiMixin.pyx",
            "flask_inputfilter/InputFilter.pyx",
        ],
        language_level=3,
    ),
)
