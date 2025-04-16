from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize(
        ["flask_inputfilter/InputFilter.pyx"], language_level=3
    ),
)
